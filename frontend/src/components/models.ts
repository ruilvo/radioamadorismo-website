export interface DimRf {
  id: number;
  tx_mhz: string; // Comes in as a string, but is a number
  rx_mhz: string; // Comes in as a string, but is a number
  channel: null | string;
  mode: string; // TODO: enum
  shift_mhz: string; // Comes in as a string, but is a number
}

export interface DimFm {
  id: number;
  modulation: string;
  tone: null | string; // Comes in as a string, but is a number
  bandwidth: string; // TODO: enum
}

export interface DimDstar {
  id: number;
  gateway: string;
  reflector: string;
}

export interface DimFusion {
  id: number;
  wiresx: string;
  room_id: string;
}

export interface DimDmrTg {
  id: number;
  name: string;
  call_mode: string; // TODO: enum
}

export interface DimDmr {
  id: number;
  tg: DimDmrTg;
  ts1_default_tg: DimDmrTg;
  ts2_default_tg: DimDmrTg;
  ts1_alternative_tgs: Array<DimDmrTg>;
  ts2_alternative_tgs: Array<DimDmrTg>;
  color_code: number;
  ts_configuration: string;
}

export interface Association {
  id: number;
  abrv: string;
  name: string;
  email: string;
  website: string;
  notes: string;
}

export interface DimLocation {
  id: number;
  latitude: null | string; // Comes in as a string, but is a number
  longitude: null | string; // Comes in as a string, but is a number
  region: string; // TODO: enum
  place: string;
  qth_loc: string;
}

export interface FactRepeater {
  id: number;
  info_rf: null | DimRf;
  info_fm: null | DimFm;
  info_dstar: null | DimDstar;
  info_fusion: null | DimFusion;
  info_dmr: null | DimDmr;
  info_holder: null | Association;
  info_location: null | DimLocation;
  callsign: string;
  notes: string;
  pwr_w: null | number;
  status: string; // TODO: enum
  sysop: string;
  modes: Array<string>; // TODO: enum
  info_tetra: null | number;
}
