
module apb_one_time_pad #(parameter int WIDTH = 128) (
    input logic clk,
    input logic rst_n,
    input logic [31:0] addr,
    input logic [WIDTH-1:0] wdata,
    input logic we,
    output logic [WIDTH-1:0] rdata
);

    logic [WIDTH-1:0] mem [0:255];

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mem <= '{default:0};
        end else if (we) begin
            mem[addr] <= wdata;
        end
    end

    always_comb begin
        rdata = mem[addr];
    end