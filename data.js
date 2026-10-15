// ランニングシューズ 3Dマップのデータ
// speed:   -5（遅い）〜 +5（速い）
// rebound: -5（低反発・安定）〜 +5（高反発）
// weight:  重さ（g）。未入力なら null
// price:   価格（円）。未入力なら null
// year:    発売年
// image:   images フォルダの画像パス（例 "images/vaporfly.webp"）。なければ null で仮のイラストを表示
// brandId: brands の id
window.SHOE_DATA = {
  "brands": [
    {
      "id": "b-adidas",
      "name": "adidas",
      "color": "#3d4450"
    },
    {
      "id": "b-asics",
      "name": "ASICS",
      "color": "#1e63c8"
    },
    {
      "id": "bmv8detj3r4eo",
      "name": "BROOKS",
      "color": "#0e7490"
    },
    {
      "id": "b-hoka",
      "name": "HOKA",
      "color": "#0f9d8a"
    },
    {
      "id": "b-mizuno",
      "name": "Mizuno",
      "color": "#5b3fc4"
    },
    {
      "id": "b-newbalance",
      "name": "New Balance",
      "color": "#5b8a1c"
    },
    {
      "id": "b-nike",
      "name": "Nike",
      "color": "#ef6c1a"
    },
    {
      "id": "bmv8debr55pba",
      "name": "On",
      "color": "#b7791f"
    },
    {
      "id": "b-puma",
      "name": "PUMA",
      "color": "#d23a2f"
    },
    {
      "id": "b-saucony",
      "name": "Saucony",
      "color": "#c92a62"
    }
  ],
  "shoes": [
    {
      "id": "smv90mb9iwtyw",
      "brandId": "b-asics",
      "name": "Sortie Magic RP 4",
      "year": 2017,
      "speed": 4.8,
      "rebound": -0.5,
      "weight": 155,
      "price": 16500,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90nl9tddik",
      "brandId": "b-asics",
      "name": "Tartherzeal 6",
      "year": 2017,
      "speed": 4,
      "rebound": -1,
      "weight": 160,
      "price": 16000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8dryd7pfeh",
      "brandId": "b-nike",
      "name": "Zoom Vaporfly 4%",
      "year": 2017,
      "speed": 1,
      "rebound": 1,
      "weight": 184,
      "price": 25920,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8ztfcurncf",
      "brandId": "b-adidas",
      "name": "Adizero Sub2",
      "year": 2018,
      "speed": 3,
      "rebound": 0.5,
      "weight": 200,
      "price": 20000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8dvj37gsga",
      "brandId": "b-nike",
      "name": "Vaporfly 4% Flyknit",
      "year": 2018,
      "speed": 1.3,
      "rebound": 1,
      "weight": 195,
      "price": 28080,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90pn75zd07",
      "brandId": "b-asics",
      "name": "Tartheredge",
      "year": 2019,
      "speed": 4.2,
      "rebound": -0.7,
      "weight": 180,
      "price": 16000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8wf7cz3i8n",
      "brandId": "b-nike",
      "name": "ZoomX Vaporfly NEXT%",
      "year": 2019,
      "speed": 2,
      "rebound": 2,
      "weight": 190,
      "price": 29700,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8zzqqh8mgu",
      "brandId": "b-adidas",
      "name": "Adios Pro",
      "year": 2020,
      "speed": 1.5,
      "rebound": 2,
      "weight": 230,
      "price": 22000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8wh5q0q6y3",
      "brandId": "b-nike",
      "name": "Air Zoom Alphafly NEXT%",
      "year": 2020,
      "speed": 4,
      "rebound": 4,
      "weight": 206,
      "price": 33000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90s0k2rw4q",
      "brandId": "b-asics",
      "name": "Metaracer",
      "year": 2020,
      "speed": 3,
      "rebound": 1,
      "weight": 190,
      "price": 20000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv901qntjff6",
      "brandId": "b-adidas",
      "name": "Adios Pro 2",
      "year": 2021,
      "speed": 2,
      "rebound": 1,
      "weight": 225,
      "price": 26000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90wikd9p74",
      "brandId": "b-asics",
      "name": "Metaspeed Edge",
      "year": 2021,
      "speed": 0.5,
      "rebound": 0.8,
      "weight": 210,
      "price": 27500,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90v2r34em7",
      "brandId": "b-asics",
      "name": "Metaspeed Sky",
      "year": 2021,
      "speed": 1,
      "rebound": 1.2,
      "weight": 199,
      "price": 27500,
      "image": null,
      "note": ""
    },
    {
      "id": "smv906vu1mboe",
      "brandId": "b-adidas",
      "name": "Takumi Sen 8",
      "year": 2021,
      "speed": 3.7,
      "rebound": 0.3,
      "weight": 190,
      "price": 20000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8wibby6kpc",
      "brandId": "b-nike",
      "name": "Vaporfly NEXT% 2",
      "year": 2021,
      "speed": 2.3,
      "rebound": 2,
      "weight": 188,
      "price": 30250,
      "image": null,
      "note": ""
    },
    {
      "id": "smv908073ylnf",
      "brandId": "b-adidas",
      "name": "Adios Pro 3",
      "year": 2022,
      "speed": 2,
      "rebound": 2.5,
      "weight": 223,
      "price": 26400,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8wl7zhxd6j",
      "brandId": "b-nike",
      "name": "Alphafly NEXT% 2",
      "year": 2022,
      "speed": 3.5,
      "rebound": 4,
      "weight": 233,
      "price": 33000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90ysu5y4x2",
      "brandId": "b-asics",
      "name": "Metaspeed Edge+",
      "year": 2022,
      "speed": 1.2,
      "rebound": 1,
      "weight": 210,
      "price": 27500,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90y0vfachk",
      "brandId": "b-asics",
      "name": "Metaspeed Sky+",
      "year": 2022,
      "speed": 1.7,
      "rebound": 2,
      "weight": 196,
      "price": 27500,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8wmqvcucvu",
      "brandId": "b-nike",
      "name": "Streakfly",
      "year": 2022,
      "speed": 4.3,
      "rebound": 0.5,
      "weight": 166,
      "price": 19800,
      "image": null,
      "note": ""
    },
    {
      "id": "smv908nxu3rwx",
      "brandId": "b-adidas",
      "name": "Adios Pro Evo 1",
      "year": 2023,
      "speed": 5,
      "rebound": 4,
      "weight": 138,
      "price": 82500,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90a96mh2y6",
      "brandId": "b-adidas",
      "name": "Takumi Sen 9",
      "year": 2023,
      "speed": 4.2,
      "rebound": 1.2,
      "weight": 190,
      "price": 20900,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8wsb9375pb",
      "brandId": "b-nike",
      "name": "Vaporfly 3",
      "year": 2023,
      "speed": 1.2,
      "rebound": 1.2,
      "weight": 186,
      "price": 29700,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8wtcrb4zox",
      "brandId": "b-nike",
      "name": "Alphafly 3",
      "year": 2024,
      "speed": 4.5,
      "rebound": 4.5,
      "weight": 198,
      "price": 39655,
      "image": null,
      "note": ""
    },
    {
      "id": "smv91137rxt7s",
      "brandId": "b-asics",
      "name": "Metaspeed Edge Paris",
      "year": 2024,
      "speed": 2.5,
      "rebound": 1.7,
      "weight": 185,
      "price": 27500,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90zuod3u7g",
      "brandId": "b-asics",
      "name": "Metaspeed Sky Paris",
      "year": 2024,
      "speed": 2.3,
      "rebound": 2.8,
      "weight": 176,
      "price": 27500,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90f4j2nya8",
      "brandId": "b-adidas",
      "name": "Takumi Sen 10",
      "year": 2024,
      "speed": 4,
      "rebound": 1,
      "weight": 200,
      "price": 22000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90buoa5jlj",
      "brandId": "b-adidas",
      "name": "Adios Pro 4",
      "year": 2025,
      "speed": 2.5,
      "rebound": 3,
      "weight": 200,
      "price": 28600,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90gzqep0gs",
      "brandId": "b-adidas",
      "name": "Adios Pro Evo 2",
      "year": 2025,
      "speed": 5,
      "rebound": 4.5,
      "weight": 138,
      "price": 82500,
      "image": null,
      "note": ""
    },
    {
      "id": "smv9158xkhovb",
      "brandId": "b-asics",
      "name": "Metaspeed Edge Tokyo",
      "year": 2025,
      "speed": 3.7,
      "rebound": 3,
      "weight": 170,
      "price": 29700,
      "image": null,
      "note": ""
    },
    {
      "id": "smv916rjoyql4",
      "brandId": "b-asics",
      "name": "Metaspeed Ray",
      "year": 2025,
      "speed": 3.2,
      "rebound": 3.2,
      "weight": 129,
      "price": 33000,
      "image": null,
      "note": ""
    },
    {
      "id": "smv913u8v801e",
      "brandId": "b-asics",
      "name": "Metaspeed Sky Tokyo",
      "year": 2025,
      "speed": 3.5,
      "rebound": 3.5,
      "weight": 170,
      "price": 29700,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90k6csm2wr",
      "brandId": "b-adidas",
      "name": "Takumi Sen 11",
      "year": 2025,
      "speed": 4.2,
      "rebound": 1.5,
      "weight": 170,
      "price": 24200,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8wv8axdt7w",
      "brandId": "b-nike",
      "name": "Vaporfly 4",
      "year": 2025,
      "speed": 3,
      "rebound": 2,
      "weight": 190,
      "price": 29700,
      "image": null,
      "note": ""
    },
    {
      "id": "smv90ipt0odx2",
      "brandId": "b-adidas",
      "name": "Adios Pro Evo 3",
      "year": 2026,
      "speed": 5,
      "rebound": 4.7,
      "weight": 97,
      "price": null,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8x19nddoiw",
      "brandId": "b-nike",
      "name": "Alphafly 4",
      "year": 2026,
      "speed": 4.5,
      "rebound": 4.5,
      "weight": 208,
      "price": null,
      "image": null,
      "note": ""
    },
    {
      "id": "smv8wwh4b9b30",
      "brandId": "b-nike",
      "name": "Streakfly 2",
      "year": 2026,
      "speed": 4.5,
      "rebound": 1,
      "weight": 126,
      "price": 26730,
      "image": null,
      "note": ""
    }
  ]
};
