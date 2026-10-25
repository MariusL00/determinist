`default_nettype none

module tt_um_deterministe_MariusL00 (
    input  wire [7:0] ui_in,    // Entrées dédiées (Pixels 0 à 7)
    output wire [7:0] uo_out,   // Sorties dédiées (Résultats vers le MCU)
    input  wire [7:0] uio_in,   // IOs bidirectionnelles (Pixel 8)
    output wire [7:0] uio_out,  // Non utilisées
    output wire [7:0] uio_oe,   // Direction des IOs (0 = Entrée)
    input  wire       ena,      // Signal d'activation
    input  wire       clk,      // Horloge (Design asynchrone pur)
    input  wire       rst_n     // Reset actif à l'état bas
);

    // ==========================================
    // 1. MAPPING DES ENTRÉES/SORTIES
    // ==========================================
    assign uio_oe  = 8'b00000000;
    assign uio_out = 8'b00000000;

    wire [8:0] p;
    assign p[7:0] = ui_in[7:0];
    assign p[8]   = uio_in[0];

    // ==========================================
    // 2. LOGIQUE BOOLÉENNE STRICTE (Pas de mathématiques)
    // ==========================================
    // Pour que la porte AND s'active, il faut que les pixels de la forme
    // soient à 1 (VRAI) ET que TOUS les autres soient à 0 (FAUX via le NOT ~).
    
    wire is_h  =  p[0] &  p[1] &  p[2] & ~p[3] & ~p[4] & ~p[5] & ~p[6] & ~p[7] & ~p[8];
    wire is_v  =  p[0] & ~p[1] & ~p[2] &  p[3] & ~p[4] & ~p[5] &  p[6] & ~p[7] & ~p[8];
    wire is_d1 =  p[0] & ~p[1] & ~p[2] & ~p[3] &  p[4] & ~p[5] & ~p[6] & ~p[7] &  p[8];
    wire is_d2 = ~p[0] & ~p[1] &  p[2] & ~p[3] &  p[4] & ~p[5] &  p[6] & ~p[7] & ~p[8];

    wire no_match = ~(is_h | is_v | is_d1 | is_d2); // 1 si aucune ligne n'est parfaite

    // ==========================================
    // 3. ENCODEUR DE PRIORITÉ (Identifiant)
    // ==========================================
    wire [2:0] pred_id;
    assign pred_id = (is_h)  ? 3'b001 :
                     (is_v)  ? 3'b010 :
                     (is_d1) ? 3'b011 :
                     (is_d2) ? 3'b100 :
                               3'b000; // Inconnu / Rejeté

    // ==========================================
    // 4. SORTIES VERS LE MCU (Télémétrie Logique)
    // ==========================================
    // On conserve les 3 bits de poids faible pour l'ID, pour que le MCU lise 
    // l'identifiant de la même manière qu'avec le NPU.
    // MAIS on remplace les 5 bits de "Score" (qui n'existe pas ici) par 
    // l'état brut des 5 portes logiques pour prouver la rigidité du système.
    
    assign uo_out = {no_match, is_d2, is_d1, is_v, is_h, pred_id};

endmodule