<!---
This file is used to generate your project datasheet. Please fill in the information below and delete any unused sections.
You can also include images in this folder and reference them in the markdown. Each image must be less than 512 kb in size.
-->
## How it works

The Deterministe 3x3 is an educational hardware baseline designed to be directly compared against the TinyNPU 3x3. Instead of using a neural network with spatial weights and thresholds, this chip uses strict, classical boolean logic (AND / NOT gates) to classify 3x3 binary pixel grids.

It acts as a physical representation of "If/Else" programming. It requires absolute perfection: a shape is only recognized if all its required pixels are exactly 1 (True) AND all background pixels are exactly 0 (False). It has zero tolerance for noise, missing pixels, or shifting. This intentionally demonstrates the "brittle" nature of classical deterministic logic when processing imperfect real-world data, contrasting with the NPU's ability to generalize.

To make the comparison perfectly transparent, the 8-bit output bus mimics the NPU's structure but outputs pure logic states instead of math scores:
* **The 3 Least Significant Bits (LSB, uo_out[2:0]):** Output the Prediction ID (matching the NPU's format).
* **The 5 Most Significant Bits (MSB, uo_out[7:3]):** Output the raw electrical state of the logic gates (`no_match`, `is_d2`, `is_d1`, `is_v`, `is_h`).

## How to test

1. Provide a 3x3 binary image using the input pins: pixels 0 to 7 on `ui_in[7:0]` and the 9th pixel on `uio_in[0]`.
2. The logic is strictly combinational; the result is immediately available on `uo_out[7:0]`.
3. Decode the 3 LSBs using a bitwise AND mask (`val & 0x07`) to get the detected shape ID:
   * `0` = Unknown / Rejected
   * `1` = Horizontal Line (-)
   * `2` = Vertical Line (|)
   * `3` = Diagonal 1 (\)
   * `4` = Diagonal 2 (/)
4. Decode the 5 MSBs by shifting the value right by 3 bits (`val >> 3`). You can read the exact boolean flags triggered by the input. If the input is imperfect (e.g., 2 pixels instead of 3), the `no_match` flag (the highest bit) will trigger instantly, and the ID will drop to `0`.

## External hardware

To fully exploit the educational aspect of this chip, it should be tested alongside the TinyNPU 3x3 using:
* A microcontroller (STM32, ESP32, or Arduino) to simultaneously feed the same pixel arrays to both the NPU and this Strict Logic chip.
* An I2C/SPI OLED display to visualize the head-to-head comparison: showing how this deterministic chip fails on noisy data while the NPU succeeds.
* Alternatively, a 9-pin DIP switch block and a set of LEDs can be used for manual, clock-less logic verification.