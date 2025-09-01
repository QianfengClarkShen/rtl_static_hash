`timescale 1ps/1ps
module simple_dp_ram # (
    parameter int DWIDTH = 64,
    parameter int DEPTH = 512
) (
    input logic clk,
    input logic [DWIDTH-1:0] wr_data,
    input logic [$clog2(DEPTH)-1:0] wr_addr,
    input logic wr_en,
    input logic [$clog2(DEPTH)-1:0] rd_addr,
    input logic rd_en,
    output logic [DWIDTH-1:0] rd_data
);
    logic [DWIDTH-1:0] mem_int[DEPTH-1:0];

    always_ff @(posedge clk) begin
        if (wr_en) mem_int[wr_addr] <= wr_data;
    end

    always_ff @(posedge clk) begin
        if (rd_en) rd_data <= mem_int[rd_addr];
    end
endmodule