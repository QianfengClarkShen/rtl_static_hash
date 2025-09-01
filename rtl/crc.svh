/**
Copyright (c) 2022, Qianfeng (Clark) Shen
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
 * @author Qianfeng (Clark) Shen
 * @email qianfeng.shen@gmail.com
 * @create date 2022-03-18 13:57:54
 * @modify date 2022-03-18 13:57:54
 */

function automatic bit [CRC_WIDTH-1:0][DWIDTH+CRC_WIDTH-1:0] gen_unified_table();
    bit [CRC_WIDTH-1:0][DWIDTH+CRC_WIDTH-1:0] table_old = {CRC_WIDTH{{(DWIDTH+CRC_WIDTH){1'b0}}}};
    bit [CRC_WIDTH-1:0][DWIDTH+CRC_WIDTH-1:0] unified_table = {CRC_WIDTH{{(DWIDTH+CRC_WIDTH){1'b0}}}};
    for (int i = 0; i < CRC_WIDTH; i++)
        table_old[i][i] = 1'b1;
    for (int i = 0; i < DWIDTH; i++) begin
        /* - crc_out[0] = crc_in[CRC_WIDTH-1] ^ din[DWIDTH-1-i]; */
        unified_table[0] = table_old[CRC_WIDTH-1];
        unified_table[0][CRC_WIDTH+DWIDTH-1-i] = ~unified_table[0][CRC_WIDTH+DWIDTH-1-i];
        /////////////////////////////////////////////////////////////
        for (int j = 1; j < CRC_WIDTH; j++) begin
            if (CRC_POLY[j])
                unified_table[j] = table_old[j-1] ^ unified_table[0];
            else
                unified_table[j] = table_old[j-1];
        end
        table_old = unified_table;
    end
    return unified_table;
endfunction

function automatic bit [CRC_WIDTH-1:0][CRC_WIDTH-1:0] gen_crc_table(
    input bit [CRC_WIDTH-1:0][DWIDTH+CRC_WIDTH-1:0] unified_table
);
    bit [CRC_WIDTH-1:0][CRC_WIDTH-1:0] crc_table;
    for (int i = 0; i < CRC_WIDTH; i++) begin
        for (int j = 0; j < CRC_WIDTH; j++)
            crc_table[i][j] = unified_table[i][j];
    end
    return crc_table;
endfunction

function automatic bit [CRC_WIDTH-1:0][DWIDTH-1:0] gen_data_table(
    input bit [CRC_WIDTH-1:0][DWIDTH+CRC_WIDTH-1:0] unified_table
);
    bit [CRC_WIDTH-1:0][DWIDTH-1:0] data_table;
    for (int i = 0; i < CRC_WIDTH; i++) begin
        for (int j = 0; j < DWIDTH; j++)
            data_table[i][j] = unified_table[i][j+CRC_WIDTH];
    end
    return data_table;
endfunction