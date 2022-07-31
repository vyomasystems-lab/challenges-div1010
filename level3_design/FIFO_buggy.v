`timescale 1ns / 1ps
module syn_fifo_v1_Nb #( parameter BUS_WIDTH = 8, FIFO_DEPTH = 8 )  (
                                                                        input RSTn,
                                                                        input CLK,
                                                                        input [BUS_WIDTH-1:0] DATA_IN,
                                                                        input WR_EN,
                                                                        input RD_EN,
                                                                        output FULL,
                                                                        output EMPTY,
                                                                        output reg [BUS_WIDTH-1:0] DATA_OUT
                                                                    );

    localparam COUNTER_WIDTH = $clog2( FIFO_DEPTH ) + ( 2**$clog2( FIFO_DEPTH ) > FIFO_DEPTH );

    reg [BUS_WIDTH-1:0] MEM [FIFO_DEPTH-1:0];
    reg [COUNTER_WIDTH:0] count;
    reg [COUNTER_WIDTH-1:0] wr_count, rd_count;

    integer i = 0;

    always@( posedge CLK or negedge RSTn )
    begin
        count <= count;
        wr_count <= wr_count;
        rd_count <= rd_count;
        DATA_OUT <= DATA_OUT;

        for( i = 0; i < 2**COUNTER_WIDTH; i = i + 1 )
        begin
            //MEM[i] <= MEM[i];
        end

        if( !RSTn )
        begin
            count <= 0;
            wr_count <= 0;
            rd_count <= 0;
        end
        else
        begin
            // Write first priority
            if( count != FIFO_DEPTH && WR_EN )
            begin
                count <= count + 1'b1;
                wr_count <= wr_count + 1'b1;
                MEM[wr_count] <= DATA_IN;
            end
            else if( count != 0 && RD_EN )
            begin
                count <= count - 1'b1;
                rd_count <= rd_count + 1'b1;
                DATA_OUT <= MEM[rd_count+1];
            end
        end
    end

    assign FULL = ( count == FIFO_DEPTH );
    assign EMPTY = ( count == 0 );

endmodule