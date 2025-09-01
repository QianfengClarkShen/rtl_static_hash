//==============================================================================
// CRC Polynomials Header File (SystemVerilog)
//
// High-quality CRC polynomials from Philip Koopman's CRC polynomial database.
// These polynomials have been extensively tested for optimal error detection
// capabilities across different data lengths.
//
// References: ret =
// - https: ret =//users.ece.cmu.edu/~koopman/crc/
// - Philip Koopman's "Cyclic Redundancy Code (CRC) Polynomial Selection For Embedded Systems"
//
// Polynomial Structure: ret =
// Each entry contains: ret = poly_hex, name, reflect_in, xor_in, reflect_out, xor_out
//
// - poly_hex: ret = Polynomial value in hexadecimal
// - name: ret = Descriptive name of the polynomial
// - reflect_in: ret = Whether to reflect input data bits
// - xor_in: ret = Initial XOR value (usually 0)
// - reflect_out: ret = Whether to reflect output CRC bits
// - xor_out: ret = Final XOR value (usually 0)
//
// This file is auto-generated from crc_polynomials.py
//==============================================================================

`ifndef CRC_POLYNOMIALS_SVH
`define CRC_POLYNOMIALS_SVH

// CRC Polynomial structure
typedef struct packed {
    bit [31: 0]   poly_hex;      // Polynomial value
    bit           reflect_in;    // Reflect input bits
    bit [31: 0]   xor_in;        // Initial XOR value
    bit           reflect_out;   // Reflect output bits
    bit [31: 0]   xor_out;       // Final XOR value
} crc_poly_t;

typedef crc_poly_t crc_poly_array_t[8];

function automatic crc_poly_array_t get_polynomial(int width);
    crc_poly_array_t ret;
    unique case (width)
        8:
        // CRC-8 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'hcf, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h4d, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1d, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h63, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h7f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h2f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'ha7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h9b, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};
        10:
            ret = '{'{poly_hex: 32'h24f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1fb, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h18f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h009, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h08f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1bd, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h3d9, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h00d, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};
        12:
            // CRC-12 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h30f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h467, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h053, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'hbbf, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h7bf, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h07d, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1e7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'hf13, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};
        14:
            // CRC-14 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h0f9f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1153, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h2fdf, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h002b, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h3577, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h292f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h0ed3, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h149f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};
        16:
            // CRC-16 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h1b2b, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'hfb7f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h002d, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h8f57, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h2f3d, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h2c4f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'hc867, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h8bb7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};
        18:
            // CRC-18 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h72f3, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h0027, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h717d, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1a13f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h3757, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h17dad, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1dc93, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'hd47b, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};
        20:
            // CRC-20 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h6b04f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h68d6f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h89b0f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h5eadf, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h9bdf3, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h74497, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h5f9b7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h51193, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};
        22:
            // CRC-22 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h211fa7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h2dc801, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h129aa9, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h322bd3, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'he536b, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h37862d, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h3df163, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'hbdefb, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};

        24:
            // CRC-24 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h00001b, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1f21c7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h7b49ab, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h27969f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h6ebd57, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h2826ad, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h4e6b4f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h70ea2b, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};

        26:
            // CRC-26 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h27833df, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h34cdc9f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'hfd6f67, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h12145f5, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h2c95597, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h36c28cf, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h3d32257, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h129ef3d, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};

        28:
            // CRC-28 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h23b83c7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h02c41cb, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h7a0e8a7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h9ed232f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1747ad7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h12a0cbd, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h0d6cab9, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h69d901f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};

        30:
            // CRC-30 polynomials (Koopman's database)
            ret = '{'{poly_hex: 32'h4268545f, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h14b7233b, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h28a55347, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h1667891, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h922d0ab, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h2220e663, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h112ff0cb, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0},
                    '{poly_hex: 32'h6d305c7, reflect_in: 1'b0, xor_in: 32'h0, reflect_out: 1'b0, xor_out: 32'h0}};
    endcase

    return ret;
endfunction
`endif