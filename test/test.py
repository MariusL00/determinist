import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_strict_logic(dut):
    """Testbench automatisé pour le circuit Déterministe Strict (If/Else)"""
    
    # 1. Initialisation des signaux
    dut.ena.value = 1
    dut.clk.value = 0
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    
    # Sortie du reset
    await Timer(10, units="ns")
    dut.rst_n.value = 1
    await Timer(10, units="ns")

    dut._log.info("Démarrage des tests du circuit Déterministe Strict...")

    id_to_name = {
        0: "REJETÉ/INCONNU", 
        1: "Horizontal", 
        2: "Vertical", 
        3: "Diagonale 1", 
        4: "Diagonale 2"
    }

    # 2. Fonction utilitaire de test et de décodage
    async def run_test(name, pixels, expected_id, expected_flags_bin):
        # Injection des pixels
        ui_in_val = sum((pixels[i] << i) for i in range(8))
        uio_in_val = pixels[8]
        
        dut.ui_in.value = ui_in_val
        dut.uio_in.value = uio_in_val
        
        # Le délai matériel d'une porte logique est quasi instantané, 
        # mais on attend 10ns pour la simulation
        await Timer(10, units="ns")
        
        # --- DÉCODAGE DE LA SORTIE ---
        uo_val = int(dut.uo_out.value)
        
        # MASQUE 1 : 3 bits de poids faible pour l'ID (Opération ET binaire)
        pred_id = uo_val & 0b111 
        
        # MASQUE 2 : 5 bits de poids fort pour l'état des portes logiques
        # Format des flags : [no_match, is_d2, is_d1, is_v, is_h]
        logic_flags = (uo_val >> 3) & 0b11111

        # Formatage binaire pour l'affichage (ex: "10000" pour no_match=1)
        flags_str = format(logic_flags, '05b')

        # --- VÉRIFICATIONS ---
        assert pred_id == expected_id, \
            f"❌ ID Erreur sur '{name}': Attendu {expected_id}, Obtenu {pred_id}"
            
        assert flags_str == expected_flags_bin, \
            f"❌ Portes Erreur sur '{name}': Attendu {expected_flags_bin}, Obtenu {flags_str}"
        
        status = "✅ SUCCÈS" if expected_id != 0 else "⚠️ REJETÉ (Attendu)"
        dut._log.info(f"{status.ljust(18)} | {name.ljust(25)} -> ID: {id_to_name[pred_id].ljust(15)} | Portes: {flags_str}")

    # 3. Scénarios de tests (Forme ID, État attendu des 5 portes logiques)
    # Rappel du format des portes : [No_Match, Diag2, Diag1, Vert, Horiz]
    
    dut._log.info("--- Tests des motifs 100% parfaits ---")
    await run_test("Ligne Horizontale (Haut)", [1,1,1, 0,0,0, 0,0,0], expected_id=1, expected_flags_bin="00001")
    await run_test("Ligne Verticale (Gauche)", [1,0,0, 1,0,0, 1,0,0], expected_id=2, expected_flags_bin="00010")
    await run_test("Diagonale 1 (\\)",         [1,0,0, 0,1,0, 0,0,1], expected_id=3, expected_flags_bin="00100")
    await run_test("Diagonale 2 (/)",          [0,0,1, 0,1,0, 1,0,0], expected_id=4, expected_flags_bin="01000")
    
    dut._log.info("--- Tests de fragilité (Le NPU réussissait, le Strict échoue) ---")
    
    # Il manque 1 pixel : La porte AND s'effondre. Le flag "no_match" (bit de gauche) passe à 1.
    await run_test("Ligne Horizontale (2px)",  [1,1,0, 0,0,0, 0,0,0], expected_id=0, expected_flags_bin="10000")
    
    # 1 pixel parasite s'allume : La porte NOT s'effondre.
    await run_test("Horizontale + 1 Parasite", [1,1,1, 0,0,1, 0,0,0], expected_id=0, expected_flags_bin="10000")
    
    # Bruit total
    await run_test("Bruit (Vide)",             [0,0,0, 0,0,0, 0,0,0], expected_id=0, expected_flags_bin="10000")
    await run_test("Bruit (Plein)",            [1,1,1, 1,1,1, 1,1,1], expected_id=0, expected_flags_bin="10000")
    
    dut._log.info("🎉 Tous les tests Stricts sont passés ! La démonstration de la fragilité de la logique classique est validée.")