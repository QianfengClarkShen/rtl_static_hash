`timescale 1ps/1ps

module static_hash #(
    parameter int CRC_WIDTH = 8,
    parameter int DATA_WIDTH = 32,
    parameter int N_CRCS = 8
) (
    input logic clk,
    input logic rst,
//AXI Lite configuration interface
//Use this interface to update the hash table
    input logic [CRC_WIDTH+4:0]   cfg_axil_awaddr,
    input logic                   cfg_axil_awvalid,
    output logic                  cfg_axil_awready,
    input logic [31:0]            cfg_axil_wdata,
    input logic [3:0]             cfg_axil_wstrb,
    input logic                   cfg_axil_wvalid,
    output logic                  cfg_axil_wready,
    output logic [1:0]            cfg_axil_bresp,
    output logic                  cfg_axil_bvalid,
    input logic                   cfg_axil_bready,
//AXI-Stream sparse input
    input logic [DATA_WIDTH-1:0]  sparse_axis_tdata,
    input logic                   sparse_axis_tvalid,
    output logic                  sparse_axis_tready,
//AXI-Stream Hashed ID output
    output logic [CRC_WIDTH-1:0]  uuid_axis_tdata,
    output logic                  uuid_axis_tvalid,
    input logic                   uuid_axis_tready
);
    `include "crc_polynomials.svh"
    parameter crc_poly_array_t crc_defs = get_polynomial(CRC_WIDTH);

    logic [N_CRCS-1:0] mem_onehot_write;
    logic [CRC_WIDTH-1:0] mem_addr;
    logic [CRC_WIDTH:0] mem_data;

    static_hash_axil #(
        .CRC_WIDTH(CRC_WIDTH)
    ) u_static_hash_axil (.*);

    logic [CRC_WIDTH-1:0] hash_val[N_CRCS-1:0];

    typedef struct packed {
        logic valid;
        logic [CRC_WIDTH-1:0] value;
    } hash_entry_t;
    hash_entry_t hash_entry[N_CRCS-1:0];

    for (genvar i = 0; i < N_CRCS; i++) begin
        simple_dp_ram #(
            .DWIDTH(CRC_WIDTH+1),
            .DEPTH(2**CRC_WIDTH)
        ) u_simple_dp_ram (
            .clk(clk),
            .wr_data(mem_data),
            .wr_addr(mem_addr[CRC_WIDTH-1:0]),
            .wr_en(mem_onehot_write[i]),
            .rd_addr(hash_val[i]),
            .rd_en(uuid_axis_tready),
            .rd_data(hash_entry[i])
        );

        simple_crc # (
            .DWIDTH(DATA_WIDTH),
            .CRC_WIDTH(CRC_WIDTH),
            .CRC_POLY(crc_defs[i].poly_hex[CRC_WIDTH-1:0]),
            .INIT(crc_defs[i].xor_in[CRC_WIDTH-1:0]),
            .XOR_OUT(crc_defs[i].xor_out[CRC_WIDTH-1:0]),
            .REFIN(crc_defs[i].reflect_in),
            .REFOUT(crc_defs[i].reflect_out)
        ) u_crc (
            .clk(clk),
            .rst(rst),
            .s_axis_tdata(sparse_axis_tdata),
            .s_axis_tvalid(sparse_axis_tvalid),
            .s_axis_tready(), //always ready
            .crc_tdata(hash_val[i]),
            .crc_tvalid(),
            .crc_tready(uuid_axis_tready)
        );
    end

    logic [CRC_WIDTH-1:0] uuid_wire;

    always_comb begin
        uuid_wire = '0;
        for (int i = 0; i < N_CRCS; i++)
            if (hash_entry[i].valid) begin
                uuid_wire = hash_entry[i].value;
                break;
            end
    end

    /*output logic
        3-cycle pipeline : input -> calculate crc -> mem_read -> register out
    */

    logic [1:0] valid_pipe_reg;

    always_ff @(posedge clk) begin
        if (rst) begin
            valid_pipe_reg <= '0;
            uuid_axis_tdata <= '0;
            uuid_axis_tvalid <= '0;
        end else begin
            if (uuid_axis_tready) begin
                uuid_axis_tdata <= uuid_wire;
                valid_pipe_reg[0] <= sparse_axis_tvalid;
                valid_pipe_reg[1] <= valid_pipe_reg[0];
                uuid_axis_tvalid <= valid_pipe_reg[1];
            end
        end
    end

    assign sparse_axis_tready = uuid_axis_tready;
endmodule