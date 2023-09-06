export function format_decimal_field(
  field: string,
  precision: number = 4,
): string {
  return Number.parseFloat(field).toFixed(precision).toString();
}

export function format_modes_field(field: readonly string[]): string {
  const modeMap: { [key: string]: string } = {
    fm: 'FM',
    dmr: 'DMR',
    dstar: 'D-Star',
    fusion: 'Fusion',
    tetra: 'TETRA',
  };
  const modes_formatted = field.map((mode) => modeMap[mode]);
  return modes_formatted.join(', ');
}

export function format_region_field(field: string): string {
  const regionMap: { [key: string]: string } = {
    CPT: 'Continente',
    AZR: 'Açores',
    MDA: 'Madeira',
    OT: '',
  };
  return regionMap[field];
}

export function format_status_field(field: string) {
  const statusMap: { [key: string]: string } = {
    OFF: 'Desligado',
    ON: 'Ligado',
    PROJECT: 'Projeto',
    PROBLEMS: 'Problemas',
    OT: 'Outro/Desconhecido',
  };
  return statusMap[field];
}
