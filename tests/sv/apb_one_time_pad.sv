
module apb_one_time_pad #(parameter int WIDTH = 128) (
    input logic pclk,
    input logic preset_n,
    input logic [31:0] paddr,
    input logic psel,
    input logic penable,
    input logic pwrite,
    input logic [2:0] pprot,
    input logic [WIDTH-1:0] pwdata,
    output logic [WIDTH-1:0] prdata,
    output logic pready
);

    logic [WIDTH-1:0] key;
    logic [WIDTH-1:0] data;
    logic [WIDTH-1:0] result;

    always_ff @(posedge pclk or negedge preset_n) begin
        if (!preset_n) begin
            key <= 0;
            data <= 0;
        end
        else begin
            if (psel && penable && (paddr == 'h0) && pwrite && pprot[0]) begin
                key <= pwdata;
            end
            else if (psel && penable && (paddr == 'h1) && pwrite) begin
                data <= pwdata;
            end
        end
    end

    always_comb begin
        if (data != '0) begin
            result = data ^ key;
        end
    end

    always_comb begin
        if (!preset_n) begin
            prdata <= 0;
            pready <= 0;
        end
        else if (psel && penable && !pwrite) begin
            pready <= 1;
            if ((paddr == 'h2) && (pprot[2:1] == 2'b00)) begin
                prdata <= result;
            end
            else begin
                prdata <= 0;
            end
        end
        else begin
            pready <= 0;
            prdata <= 0;
        end
    end
endmodule