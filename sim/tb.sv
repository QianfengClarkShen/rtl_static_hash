`timescale 1ps/1ps

module tb #(
    parameter string IN_FILE = "input.txt",
    parameter int CRC_WIDTH = 8,
    parameter int DATA_WIDTH = 32
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
    input logic [CRC_WIDTH+4:0]   cfg_axil_araddr,
    input logic         cfg_axil_arvalid,
    output logic        cfg_axil_arready,
    output logic [31:0] cfg_axil_rdata,
    output logic [1:0]  cfg_axil_rresp,
    output logic        cfg_axil_rvalid,
    input logic         cfg_axil_rready,
//AXI-Stream sparse input (make it byte_aligned)
    input logic [(DATA_WIDTH-1)/8*8+7:0]  sparse_axis_tdata,
    input logic                   sparse_axis_tvalid,
    output logic                  sparse_axis_tready,
//AXI-Stream Hashed ID output (make it byte aligned)
    output logic [(CRC_WIDTH-1)/8*8+7:0]  uuid_axis_tdata,
    output logic                  uuid_axis_tvalid,
    input logic                   uuid_axis_tready,
    output logic                  hash_err
);
    logic [DATA_WIDTH-1:0] sparse_axis_data_tmp;
    logic [CRC_WIDTH-1:0] uuid_axis_data_tmp;

    static_hash # (
        .CRC_WIDTH(CRC_WIDTH),
        .DATA_WIDTH(DATA_WIDTH)
    ) u_static_hash (
        .*,
        .sparse_axis_tdata(sparse_axis_data_tmp),
        .uuid_axis_tdata(uuid_axis_data_tmp)
    );
    always_comb begin
        uuid_axis_tdata = '0;
        uuid_axis_tdata[CRC_WIDTH-1:0] = uuid_axis_data_tmp;
    end

    assign sparse_axis_data_tmp = sparse_axis_tdata[DATA_WIDTH-1:0];

    assign cfg_axil_arready = '0;
    assign cfg_axil_rdata = '0;
    assign cfg_axil_rresp = '0;
    assign cfg_axil_rvalid = '0;

endmodule