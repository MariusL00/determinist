`default_nettype none
`timescale 1ns / 1ps

/* Ce fichier généré automatiquement connecte votre module au simulateur Python. 
   Vous n'avez pas besoin de le modifier. */

module tb ();
    // Configuration pour générer le graphique des ondes (GTKWave)
    initial begin
        $dumpfile("tb.vcd");
        $dumpvars(0, tb);
        #1;
    end

    // Déclaration des signaux
    reg clk;
    reg rst_n;
    reg ena;
    reg [7:0] ui_in;
    reg [7:0] uio_in;
    wire [7:0] uo_out;
    wire [7:0] uio_out;
    wire [7:0] uio_oe;

    // ==========================================
    // AJOUTE CES DEUX LIGNES ICI :
    // ==========================================
    wire VPWR = 1'b1;
    wire VGND = 1'b0;

    // Instanciation de votre circuit
    tt_um_deterministe_MariusL00 user_project (
        .ui_in  (ui_in),
        .uo_out (uo_out),
        .uio_in (uio_in),
        .uio_out(uio_out),
        .uio_oe (uio_oe),
        .ena    (ena),
        .clk    (clk),
        .rst_n  (rst_n)
`ifdef USE_POWER_PINS
        ,
        .VPWR(VPWR),  // Le port bidirectionnel est maintenant relié au "wire"
        .VGND(VGND)   // Le port bidirectionnel est maintenant relié au "wire"
`endif
    );
endmodule
