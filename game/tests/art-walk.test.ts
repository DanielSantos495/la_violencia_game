import { describe, expect, it } from 'vitest';
import { hojaCaminata } from '../tools/art-walk.ts';

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 200">
  <g id="pierna-der" data-pieza="" data-pivote="50 100"><rect x="45" y="100" width="10" height="90"/></g>
  <g id="brazo-der" data-pieza="" data-pivote="50 40"><rect x="45" y="40" width="10" height="40"/></g>
  <g id="antebrazo-der" data-pieza="" data-pivote="50 80" data-padre="brazo-der"><rect x="45" y="80" width="10" height="30"/></g>
</svg>`;

describe('hojaCaminata', () => {
  it('dibuja una celda por fase con la pose aplicada y la jerarquía del SVG', () => {
    const hoja = hojaCaminata(svg, 'p', 4);
    expect(hoja).toContain('width="400"');
    expect(hoja.match(/stroke-dasharray="3 3"/g)).toHaveLength(4);
    // El antebrazo hereda primero la rotación del brazo (en su pivote) y luego la suya.
    expect(hoja).toMatch(
      /id="antebrazo-der"[^>]*transform="rotate\([-\d.]+ 50 40\) rotate\([-\d.]+ 50 80\)"/,
    );
  });
});
