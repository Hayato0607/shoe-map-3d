// ランニングシューズ 3Dマップのデータ
// speed:   -5（遅い）〜 +5（速い）
// rebound: -5（低反発・安定）〜 +5（高反発）
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
      "id": "s01",
      "brandId": "b-nike",
      "name": "Cortez",
      "year": 1972,
      "speed": -2,
      "rebound": -4.5,
      "image": null,
      "note": ""
    },
    {
      "id": "s02",
      "brandId": "b-nike",
      "name": "Air Pegasus",
      "year": 1983,
      "speed": -1.5,
      "rebound": -3,
      "image": null,
      "note": ""
    },
    {
      "id": "s03",
      "brandId": "b-asics",
      "name": "GEL-KAYANO",
      "year": 1993,
      "speed": -2.5,
      "rebound": -4,
      "image": null,
      "note": ""
    },
    {
      "id": "s04",
      "brandId": "b-adidas",
      "name": "adizero Adios",
      "year": 2008,
      "speed": 3.5,
      "rebound": -2.5,
      "image": null,
      "note": ""
    },
    {
      "id": "s05",
      "brandId": "b-adidas",
      "name": "Ultraboost",
      "year": 2015,
      "speed": -3,
      "rebound": 1,
      "image": null,
      "note": ""
    },
    {
      "id": "s06",
      "brandId": "b-nike",
      "name": "Zoom Vaporfly 4%",
      "year": 2017,
      "speed": 4.5,
      "rebound": 4,
      "image": null,
      "note": ""
    },
    {
      "id": "s07",
      "brandId": "b-nike",
      "name": "ZoomX Alphafly NEXT%",
      "year": 2020,
      "speed": 5,
      "rebound": 4.8,
      "image": null,
      "note": ""
    },
    {
      "id": "s08",
      "brandId": "b-asics",
      "name": "METASPEED Sky",
      "year": 2021,
      "speed": 4.5,
      "rebound": 3.8,
      "image": null,
      "note": ""
    },
    {
      "id": "s09",
      "brandId": "b-adidas",
      "name": "Adizero Adios Pro 3",
      "year": 2022,
      "speed": 4.6,
      "rebound": 4.2,
      "image": null,
      "note": ""
    },
    {
      "id": "s10",
      "brandId": "b-saucony",
      "name": "Endorphin Pro 3",
      "year": 2022,
      "speed": 4.2,
      "rebound": 3.6,
      "image": null,
      "note": ""
    },
    {
      "id": "s11",
      "brandId": "b-mizuno",
      "name": "Wave Rebellion Pro",
      "year": 2022,
      "speed": 3.6,
      "rebound": 2.6,
      "image": null,
      "note": ""
    },
    {
      "id": "s12",
      "brandId": "b-puma",
      "name": "Fast-R Nitro Elite",
      "year": 2022,
      "speed": 4.4,
      "rebound": 4,
      "image": null,
      "note": ""
    },
    {
      "id": "s13",
      "brandId": "b-nike",
      "name": "Pegasus 40",
      "year": 2023,
      "speed": 0,
      "rebound": 0,
      "image": null,
      "note": ""
    },
    {
      "id": "s14",
      "brandId": "b-asics",
      "name": "GEL-KAYANO 30",
      "year": 2023,
      "speed": -3,
      "rebound": -2.5,
      "image": null,
      "note": ""
    },
    {
      "id": "s15",
      "brandId": "b-hoka",
      "name": "Clifton 9",
      "year": 2023,
      "speed": -1.5,
      "rebound": 1.2,
      "image": null,
      "note": ""
    },
    {
      "id": "s16",
      "brandId": "b-hoka",
      "name": "Rocket X 2",
      "year": 2023,
      "speed": 4,
      "rebound": 3.4,
      "image": null,
      "note": ""
    },
    {
      "id": "s17",
      "brandId": "b-adidas",
      "name": "Adizero Boston 12",
      "year": 2023,
      "speed": 2.6,
      "rebound": 2.2,
      "image": null,
      "note": ""
    },
    {
      "id": "s18",
      "brandId": "b-newbalance",
      "name": "Fresh Foam X 1080v13",
      "year": 2023,
      "speed": -1,
      "rebound": 0.6,
      "image": null,
      "note": ""
    },
    {
      "id": "s19",
      "brandId": "b-asics",
      "name": "NOVABLAST 4",
      "year": 2024,
      "speed": 0.6,
      "rebound": 3,
      "image": null,
      "note": ""
    }
  ]
};
