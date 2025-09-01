module static_hash_axil #(
    parameter int CRC_WIDTH = 8
) (
    input logic clk,
    input logic rst,
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
    output logic [7:0]            mem_onehot_write,
    output logic [CRC_WIDTH-1:0]  mem_addr,
    output logic [CRC_WIDTH:0]    mem_data
);

    localparam bit [1:0] WRIDLE = 2'd0;
    localparam bit [1:0] WRDATA = 2'd1;
    localparam bit [1:0] WRRESP = 2'd2;
    localparam bit [1:0] WRRESET = 2'd3;
    localparam int ADDR_BITS = CRC_WIDTH + 5;

    logic [1:0] wstate;
    logic [1:0] wnext;
    logic [ADDR_BITS-1:0] waddr;
    logic [31:0] wmask;
    logic aw_hs;
    logic w_hs;

    //------------------------AXI write fsm-------------------
    assign cfg_axil_awready = (wstate == WRIDLE);
    assign cfg_axil_wready = (wstate == WRDATA);
    assign cfg_axil_bresp = 2'b00;
    assign cfg_axil_bvalid = (wstate == WRRESP);
    assign wmask = { {8{cfg_axil_wstrb[3]}}, {8{cfg_axil_wstrb[2]}}, {8{cfg_axil_wstrb[1]}}, {8{cfg_axil_wstrb[0]}} };
    assign aw_hs = cfg_axil_awvalid & cfg_axil_awready;
    assign w_hs = cfg_axil_wvalid & cfg_axil_wready;

// wstate
    always_ff @(posedge clk) begin
        if (rst)
            wstate <= WRRESET;
        else
            wstate <= wnext;
    end

    // wnext
    always_comb begin
        case (wstate)
            WRIDLE:
                if (cfg_axil_awvalid)
                    wnext = WRDATA;
                else
                    wnext = WRIDLE;
            WRDATA:
                if (cfg_axil_wvalid)
                    wnext = WRRESP;
                else
                    wnext = WRDATA;
            WRRESP:
                if (cfg_axil_bready)
                    wnext = WRIDLE;
                else
                    wnext = WRRESP;
            default:
                wnext = WRIDLE;
        endcase
    end

    // waddr
    always_ff @(posedge clk) begin
        if (aw_hs)
            waddr <= cfg_axil_awaddr;
    end

    //------------------------user write logic-----------------
    logic [31:0] mem_data_int;
    always_ff @(posedge clk) begin
        if (rst) begin
            mem_onehot_write <= '0;
            mem_addr <= '0;
            mem_data_int <= '0;
        end
        else if (w_hs) begin
            for (int i = 0; i < 8; i++)
                mem_onehot_write[i] <= waddr[CRC_WIDTH+4-:3] == i ? 1'b1 : 1'b0;
            mem_addr <= waddr[CRC_WIDTH+1:2];
            mem_data_int <= (cfg_axil_wdata[31:0] & wmask) | (mem_data & ~wmask);
        end
    end
    assign mem_data = mem_data_int[CRC_WIDTH:0];
endmodule