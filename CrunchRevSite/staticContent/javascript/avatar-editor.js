console.log('AVATAR EDITOR LOADING...');
console.log('VERSION 4.4.2');

document.addEventListener("DOMContentLoaded", function() {
    var avatarImage = document.getElementById("avatarImg");
    const redrawBtn = document.getElementById("redrawBtn");

    let pressedReDraw = false;

    const assetTypes = {
        "Image": 1,
        "TeeShirt": 2,
        "TShirt": 2,
        "Audio": 3,
        "Mesh": 4,
        "Lua": 5,
        "Hat": 8,
        "Place": 9,
        "Model": 10,
        "Shirt": 11,
        "Pants": 12,
        "Decal": 13,
        "Head": 17,
        "Face": 18,
        "Gear": 19,
        "Badge": 21,
        "Animation": 24,
        "Torso": 27,
        "Right Arm": 28,
        "Left Arm": 29,
        "Left Leg": 30,
        "Right Leg": 31,
        "Package": 32,
        "Game Pass": 34,
        "Plugin": 38,
        "Solid Model": 39,
        "Mesh Part": 40,
        "Hair Accessory": 41,
        "Face Accessory": 42,
        "Neck Accessory": 43,
        "Shoulder Accessory": 44,
        "Front Accessory": 45,
        "Back Accessory": 46,
        "Waist Accessory": 47,
        "Climb Animation": 48,
        "Death Animation": 49,
        "Fall Animation": 50,
        "Idle Animation": 51,
        "Jump Animation": 52,
        "Run Animation": 53,
        "Swim Animation": 54,
        "Walk Animation": 55,
        "Pose Animation": 56,
        "Special": 500
    };

    const brickColorPalette = {
        1: "#F2F3F3", // White
        2: "#A1A5A2", // Grey
        3: "#F9E999", // Light yellow
        5: "#D7C59A", // Brick yellow
        6: "#C2DAB8", // Light green (Mint)
        9: "#E8BAC8", // Light reddish violet
        11: "#80BBDB", // Pastel Blue
        12: "#CB8442", // Light orange brown
        18: "#CC8E69", // Nougat
        21: "#C4281C", // Bright red
        22: "#C470A0", // Med. reddish violet
        23: "#0D69AC", // Bright blue
        24: "#F5CD30", // Bright yellow
        25: "#624732", // Earth orange
        26: "#1B2A35", // Black
        27: "#6D6E6C", // Dark grey
        28: "#287F47", // Dark green
        29: "#A1C48C", // Medium green
        36: "#F3CF9B", // Lig. Yellowich orange
        37: "#4B974B", // Bright green
        38: "#A05F35", // Dark orange
        39: "#C1CADE", // Light bluish violet
        40: "#ECECEC", // Transparent
        41: "#CD544B", // Tr. Red
        42: "#C1DFF0", // Tr. Lg blue
        43: "#7BB6E8", // Tr. Blue
        44: "#F7F18D", // Tr. Yellow
        45: "#B4D2E4", // Light blue
        47: "#D9856C", // Tr. Flu. Reddish orange
        48: "#84B68D", // Tr. Green
        49: "#F8F184", // Tr. Flu. Green
        50: "#ECE8DE", // Phosph. White
        100: "#EEC4B6", // Light red
        101: "#DA867A", // Medium red
        102: "#6E99CA", // Medium blue
        103: "#C7C1B7", // Light grey
        104: "#6B327C", // Bright violet
        105: "#E29B40", // Br. yellowish orange
        106: "#DA8541", // Bright orange
        107: "#008F9C", // Bright bluish green
        108: "#685C43", // Earth yellow
        110: "#435493", // Bright bluish violet
        111: "#BFB7B1", // Tr. Brown
        112: "#6874AC", // Medium bluish violet
        113: "#E5ADC8", // Tr. Medi. reddish violet
        115: "#C7D23C", // Med. yellowish green
        116: "#55A5AF", // Med. bluish green
        118: "#B7D7D5", // Light bluish green
        119: "#A4BD47", // Br. yellowish green
        120: "#D9E4A7", // Lig. yellowish green
        121: "#E7AC58", // Med. yellowish orange
        123: "#D36F4C", // Br. reddish orange
        124: "#923978", // Bright reddish violet
        125: "#EAB892", // Light orange
        126: "#A5A5CB", // Tr. Bright bluish violet
        127: "#DCBC81", // Gold
        128: "#AE7A59", // Dark nougat
        131: "#9CA3A8", // Silver
        133: "#D5733D", // Neon orange
        134: "#D8DD56", // Neon green
        135: "#74869D", // Sand blue
        136: "#877C90", // Sand violet
        137: "#E09864", // Medium orange
        138: "#958A73", // Sand yellow
        140: "#203A56", // Earth blue
        141: "#27462D", // Earth green
        143: "#CFE2F7", // Tr. Flu. Blue
        145: "#7988A1", // Sand blue metallic
        146: "#958EA3", // Sand violet metallic
        147: "#938767", // Sand yellow metallic
        148: "#575857", // Dark grey metallic
        149: "#161D32", // Black metallic
        150: "#ABADAC", // Light grey metallic
        151: "#789082", // Sand green
        153: "#957977", // Sand red
        154: "#7B2E2F", // Dark red
        157: "#FFF67B", // Tr. Flu. Yellow
        158: "#E1A4C2", // Tr. Flu. Red
        168: "#756C62", // Gun metallic
        176: "#97695B", // Red flip/flop
        178: "#B48455", // Yellow flip/flop
        179: "#898788", // Silver flip/flop
        180: "#D7A94B", // Curry
        190: "#F9D62E", // Fire Yellow
        191: "#E8AB2D", // Flame yellowish orange
        192: "#694028", // Reddish brown
        193: "#CF6024", // Flame reddish orange
        194: "#A3A2A5", // Medium stone grey
        195: "#4667A4", // Royal blue
        196: "#23478B", // Dark Royal blue
        198: "#8E4285", // Bright reddish lilac
        199: "#63605F", // Dark stone grey
        200: "#828A5D", // Lemon metalic
        208: "#E5E4DF", // Light stone grey
        209: "#B08E44", // Dark Curry
        210: "#709578", // Faded green
        211: "#79B5B5", // Turquoise
        212: "#9FC3E9", // Light Royal blue
        213: "#6C81B7", // Medium Royal blue
        216: "#904C2A", // Rust
        217: "#7C5C46", // Brown
        218: "#966F9F", // Reddish lilac
        219: "#6B629B", // Lilac
        220: "#A7A9CE", // Light lilac
        221: "#CD6298", // Bright purple
        222: "#E4ADCA", // Light purple
        223: "#DC9095", // Light pink
        224: "#F0D5A0", // Light brick yellow
        225: "#EBAF7F", // Warm yellowish orange
        226: "#FDEB8D", // Cool yellow
        232: "#7DBBDD", // Dove blue
        268: "#342B75", // Medium lilac
        301: "#506D54", // Slime green
        302: "#5B5D69", // Smoky grey
        303: "#0010B0", // Dark blue
        304: "#2C651D", // Parsley green
        305: "#527CAE", // Steel blue
        306: "#335882", // Storm blue
        307: "#102ADC", // Lapis
        308: "#3D1585", // Dark indigo
        309: "#348E40", // Sea green
        310: "#5B9A4C", // Shamrock
        311: "#9FA1AC", // Fossil
        312: "#592259", // Mulberry
        313: "#1F801D", // Forest green
        314: "#9FADC0", // Cadet blue
        315: "#0989CF", // Electric blue
        316: "#7B007B", // Eggplant
        317: "#7C9C6B", // Moss
        318: "#8AAC85", // Artichoke
        319: "#B9C4B1", // Sage green
        320: "#CACBD1", // Ghost grey
        321: "#A75E9B", // Lilac
        322: "#7B2F7B", // Plum
        323: "#94BE81", // Olivine
        324: "#A8BD99", // Laurel green
        325: "#DFDFDE", // Quill grey
        327: "#970000", // Crimson
        328: "#B1E5A6", // Mint
        329: "#98C2DB", // Baby blue
        330: "#FF98DC", // Carnation pink
        331: "#FF5959", // Persimmon
        332: "#750000", // Maroon
        333: "#EFBA38", // Gold
        334: "#F8D76D", // Daisy orange
        335: "#E7E7EC", // Pearl
        336: "#C7D4E4", // Fog
        337: "#FF9494", // Salmon
        338: "#BE6862", // Terra Cotta
        339: "#562424", // Cocoa
        340: "#F1E7C7", // Wheat
        341: "#FEF3BB", // Buttermilk
        342: "#E0B2D0", // Mauve
        343: "#D490BD", // Sunrise
        344: "#965555", // Tawny
        345: "#8F4C2A", // Rust
        346: "#D3BE96", // Cashmere
        347: "#E2DCBC", // Khaki
        348: "#EDEAEA", // Lily white
        349: "#E9DADA", // Seashell
        350: "#883E3E", // Burgundy
        351: "#BC9B5D", // Cork
        352: "#C7AC78", // Burlap
        353: "#CABFA3", // Beige
        354: "#BBB3B2", // Oyster
        355: "#6C584B", // Pine Cone
        356: "#A0844F", // Fawn brown
        357: "#948988", // Hurricane grey
        358: "#ABA89E", // Cloudy grey
        359: "#AF9483", // Linen
        360: "#966766", // Copper
        361: "#564236", // Dirt brown
        362: "#7E6A3F", // Bronze
        363: "#69665C", // Flint
        364: "#5A4C42", // Dark taupe
        365: "#6A3909", // Burnt Sienna
        1001: "#F8F8F8", // Institutional white
        1002: "#CDCDCD", // Mid gray
        1003: "#111111", // Really black
        1004: "#FF0000", // Really red
        1005: "#FFB000", // Deep orange
        1006: "#B480FF", // Alder
        1007: "#A34B4B", // Dusty Rose
        1008: "#C1BE42", // Olive
        1009: "#FFFF00", // New Yeller
        1010: "#0000FF", // Really blue
        1011: "#002060", // Navy blue
        1012: "#2154B9", // Deep blue
        1013: "#04AFEC", // Cyan
        1014: "#AA5500", // CGA brown
        1015: "#AA00AA", // Magenta
        1016: "#FF66CC", // Pink
        1017: "#FFAF00", // Deep orange
        1018: "#12EED4", // Teal
        1019: "#00FFFF", // Toothpaste
        1020: "#00FF00", // Lime green
        1021: "#3A7D15", // Camo
        1022: "#7F8E64", // Grime
        1023: "#8C5B9F", // Lavender
        1024: "#AFDDFF", // Pastel light blue
        1025: "#FFC9C9", // Pastel orange
        1026: "#B1A7FF", // Pastel violet
        1027: "#9FF3E9", // Pastel blue-green
        1028: "#CCFFCC", // Pastel green
        1029: "#FFFFCC", // Pastel yellow
        1030: "#FFCC99", // Pastel brown
        1031: "#6225D1", // Royal purple
        1032: "#FF00BF"  // Hot pink
    };

    const brickColorNames = {
        1: "White",
        2: "Grey",
        3: "Light yellow",
        5: "Brick yellow",
        6: "Light green (Mint)",
        9: "Light reddish violet",
        11: "Pastel Blue",
        12: "Light orange brown",
        18: "Nougat",
        21: "Bright red",
        22: "Med. reddish violet",
        23: "Bright blue",
        24: "Bright yellow",
        25: "Earth orange",
        26: "Black",
        27: "Dark grey",
        28: "Dark green",
        29: "Medium green",
        36: "Lig. Yellowich orange",
        37: "Bright green",
        38: "Dark orange",
        39: "Light bluish violet",
        40: "Transparent",
        41: "Tr. Red",
        42: "Tr. Lg blue",
        43: "Tr. Blue",
        44: "Tr. Yellow",
        45: "Light blue",
        47: "Tr. Flu. Reddish orange",
        48: "Tr. Green",
        49: "Tr. Flu. Green",
        50: "Phosph. White",
        100: "Light red",
        101: "Medium red",
        102: "Medium blue",
        103: "Light grey",
        104: "Bright violet",
        105: "Br. yellowish orange",
        106: "Bright orange",
        107: "Bright bluish green",
        108: "Earth yellow",
        110: "Bright bluish violet",
        111: "Tr. Brown",
        112: "Medium bluish violet",
        113: "Tr. Medi. reddish violet",
        115: "Med. yellowish green",
        116: "Med. bluish green",
        118: "Light bluish green",
        119: "Br. yellowish green",
        120: "Lig. yellowish green",
        121: "Med. yellowish orange",
        123: "Br. reddish orange",
        124: "Bright reddish violet",
        125: "Light orange",
        126: "Tr. Bright bluish violet",
        127: "Gold",
        128: "Dark nougat",
        131: "Silver",
        133: "Neon orange",
        134: "Neon green",
        135: "Sand blue",
        136: "Sand violet",
        137: "Medium orange",
        138: "Sand yellow",
        140: "Earth blue",
        141: "Earth green",
        143: "Tr. Flu. Blue",
        145: "Sand blue metallic",
        146: "Sand violet metallic",
        147: "Sand yellow metallic",
        148: "Dark grey metallic",
        149: "Black metallic",
        150: "Light grey metallic",
        151: "Sand green",
        153: "Sand red",
        154: "Dark red",
        157: "Tr. Flu. Yellow",
        158: "Tr. Flu. Red",
        168: "Gun metallic",
        176: "Red flip/flop",
        178: "Yellow flip/flop",
        179: "Silver flip/flop",
        180: "Curry",
        190: "Fire Yellow",
        191: "Flame yellowish orange",
        192: "Reddish brown",
        193: "Flame reddish orange",
        194: "Medium stone grey",
        195: "Royal blue",
        196: "Dark Royal blue",
        198: "Bright reddish lilac",
        199: "Dark stone grey",
        200: "Lemon metalic",
        208: "Light stone grey",
        209: "Dark Curry",
        210: "Faded green",
        211: "Turquoise",
        212: "Light Royal blue",
        213: "Medium Royal blue",
        216: "Rust",
        217: "Brown",
        218: "Reddish lilac",
        219: "Lilac",
        220: "Light lilac",
        221: "Bright purple",
        222: "Light purple",
        223: "Light pink",
        224: "Light brick yellow",
        225: "Warm yellowish orange",
        226: "Cool yellow",
        232: "Dove blue",
        268: "Medium lilac",
        301: "Slime green",
        302: "Smoky grey",
        303: "Dark blue",
        304: "Parsley green",
        305: "Steel blue",
        306: "Storm blue",
        307: "Lapis",
        308: "Dark indigo",
        309: "Sea green",
        310: "Shamrock",
        311: "Fossil",
        312: "Mulberry",
        313: "Forest green",
        314: "Cadet blue",
        315: "Electric blue",
        316: "Eggplant",
        317: "Moss",
        318: "Artichoke",
        319: "Sage green",
        320: "Ghost grey",
        321: "Lilac",
        322: "Plum",
        323: "Olivine",
        324: "Laurel green",
        325: "Quill grey",
        327: "Crimson",
        328: "Mint",
        329: "Baby blue",
        330: "Carnation pink",
        331: "Persimmon",
        332: "Maroon",
        333: "Gold",
        334: "Daisy orange",
        335: "Pearl",
        336: "Fog",
        337: "Salmon",
        338: "Terra Cotta",
        339: "Cocoa",
        340: "Wheat",
        341: "Buttermilk",
        342: "Mauve",
        343: "Sunrise",
        344: "Tawny",
        345: "Rust",
        346: "Cashmere",
        347: "Khaki",
        348: "Lily white",
        349: "Seashell",
        350: "Burgundy",
        351: "Cork",
        352: "Burlap",
        353: "Beige",
        354: "Oyster",
        355: "Pine Cone",
        356: "Fawn brown",
        357: "Hurricane grey",
        358: "Cloudy grey",
        359: "Linen",
        360: "Copper",
        361: "Dirt brown",
        362: "Bronze",
        363: "Flint",
        364: "Dark taupe",
        365: "Burnt Sienna",
        1001: "Institutional white",
        1002: "Mid gray",
        1003: "Really black",
        1004: "Really red",
        1005: "Deep orange",
        1006: "Alder",
        1007: "Dusty Rose",
        1008: "Olive",
        1009: "New Yeller",
        1010: "Really blue",
        1011: "Navy blue",
        1012: "Deep blue",
        1013: "Cyan",
        1014: "CGA brown",
        1015: "Magenta",
        1016: "Pink",
        1017: "Deep orange",
        1018: "Teal",
        1019: "Toothpaste",
        1020: "Lime green",
        1021: "Camo",
        1022: "Grime",
        1023: "Lavender",
        1024: "Pastel light blue",
        1025: "Pastel orange",
        1026: "Pastel violet",
        1027: "Pastel blue-green",
        1028: "Pastel green",
        1029: "Pastel yellow",
        1030: "Pastel brown",
        1031: "Royal purple",
        1032: "Hot pink"
    };

    const partColorMapping = {
        "color-block-head": 1,
        "color-block-torso": 1,
        "color-block-left-arm": 1,
        "color-block-right-arm": 1,
        "color-block-left-leg": 1,
        "color-block-right-leg": 1
    };

    let selectedPartClass = "";

    // let isReRendering = false;

    async function requestReRender() {
        // isReRendering = true;

        const initSource = avatarImage.src;

        avatarImage.src = `/staticContent/loading.gif`;

        const rerenderfetch = await fetch('/api/editor/avatar/rerender');

        if (!rerenderfetch.ok) {
            avatarImage.src = initSource;
            // isReRendering = false;
            return;
        }

        // if (isReRendering) return;

        const jsonFetch = await rerenderfetch.json();

        if (jsonFetch.success) {
            avatarImage.src = jsonFetch.image;
        } else {
            avatarImage.src = initSource;
        }

        // isReRendering = false;
    }

    async function loadItems() {
        try {
            const fetchResponse = await fetch('/api/editor/fetch');
            if (!fetchResponse.ok) {
                throw new Error(`HTTP error! status: ${fetchResponse.status}`);
            }

            const fetchResultText = await fetchResponse.text();
            let fetchResult;
            try {
                fetchResult = JSON.parse(fetchResultText);
            } catch (jsonError) {
                throw new Error('Invalid JSON response');
            }

            const templateDiv = document.querySelector('.card.d-none');
            const itemsContainer = document.querySelector('.item-container');
            const wearingContainer = document.querySelector('.currently-wearing-container');

            for (const item of fetchResult.items) {
                const itemInfoResponse = await fetch('/api/editor/item/info', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ itemId: item.id })
                });

                if (!itemInfoResponse.ok) {
                    throw new Error(`HTTP error! status: ${itemInfoResponse.status}`);
                }

                const itemInfoText = await itemInfoResponse.text();
                let itemInfo;
                try {
                    itemInfo = JSON.parse(itemInfoText);
                } catch (jsonError) {
                    throw new Error('Invalid JSON response');
                }

                const itemDiv = templateDiv.cloneNode(true);
                const assetTypeName = Object.keys(assetTypes).find(key => assetTypes[key] === item.assetType) || 'Unknown';

                const imgElement = itemDiv.querySelector('.card-img-top');
                imgElement.src = itemInfo.image;

                const titleElement = itemDiv.querySelector('.card-title');
                titleElement.textContent = itemInfo.name;

                const typeElement = itemDiv.querySelector('.card-text');
                typeElement.textContent = `Type: ${assetTypeName}`;

                const button = itemDiv.querySelector('.btn');
                button.textContent = item.equipped ? 'Un-Equip' : 'Equip';
                button.classList.toggle('btn-secondary', item.equipped);
                button.classList.toggle('btn-primary', !item.equipped);

                button.addEventListener('click', () => toggleItem(item.id, item.equipped, button, itemDiv));

                if (item.equipped) {
                    wearingContainer.appendChild(itemDiv);
                } else {
                    itemsContainer.appendChild(itemDiv);
                }

                itemDiv.classList.remove('d-none');
            }
        } catch (error) {
            console.log('Oh shit...');
            console.error('Error loading items:', error.message);
            alert('Failed to load items: ' + error.message + '. The page will refresh when you close this message.');
            console.log('Code has gone brrr, rebooting!');
            location.reload();
        }
    }

    async function loadAvatarBodyColors() {
        var loadingImage = document.getElementById("lc2");

        try {
            const colorResponse = await fetch('/api/editor/bodycolors/fetch');
            if (!colorResponse.ok) {
                throw new Error(`HTTP error! status: ${colorResponse.status}`);
            }

            const colorResultText = await colorResponse.text();
            let colorResult;
            try {
                colorResult = JSON.parse(colorResultText);
            } catch (jsonError) {
                throw new Error('Invalid JSON response');
            }

            colorResult.colors.forEach(color => {
                const brickColorHex = brickColorPalette[color.brickcolor] || '#a1a1a1';
                const partClass = `.color-block-${color.type.toLowerCase()}`;
                const partElement = document.querySelector(partClass);
                if (partElement) {
                    partElement.style.backgroundColor = brickColorHex;
                    partColorMapping[partClass.substring(1)] = color.brickcolor;
                }
            });

            if (loadingImage) {
                loadingImage.classList.add("d-none");
            }
        } catch (error) {
            if (loadingImage) {
                loadingImage.classList.add("d-none");
            }

            console.log('Oh shit...');
            console.error('Error loading avatar body colors:', error.message);
            alert('Failed to load avatar body colors: ' + error.message);
        }
    }

    async function toggleItem(itemId, currentlyEquipped, button, itemDiv) {
        const action = currentlyEquipped ? 1 : 0;
        try {
            const response = await fetch('/api/editor/items', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ items: [itemId], action })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const itemsContainer = document.querySelector('.item-container');
            const wearingContainer = document.querySelector('.currently-wearing-container');

            if (currentlyEquipped) {
                itemsContainer.appendChild(itemDiv);
                button.textContent = 'Equip';
                button.classList.remove('btn-secondary');
                button.classList.add('btn-primary');
            } else {
                wearingContainer.appendChild(itemDiv);
                button.textContent = 'Un-Equip';
                button.classList.remove('btn-primary');
                button.classList.add('btn-secondary');
            }

            button.replaceWith(button.cloneNode(true));
            button = itemDiv.querySelector('.btn');
            button.addEventListener('click', () => toggleItem(itemId, !currentlyEquipped, button, itemDiv));

            await requestReRender();
        } catch (error) {
            console.log('Oh shit...');
            console.error('Error toggling item:', error.message);
            alert('Failed to toggle item: ' + error.message);
        }
    }

    async function loadAvatarType() {
        var loadingImage = document.getElementById("lc1");

        try {
            const response = await fetch('/api/editor/type/fetch');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.success) {
                const avatarType = data.avatarType;
                const radioButton = document.querySelector(`input[name="flexRadioDefault"][value="${avatarType}"]`);
                if (radioButton) {
                    radioButton.checked = true;
                }
                if (loadingImage) {
                    loadingImage.classList.add("d-none");
                }
            }
        } catch (error) {
            if (loadingImage) {
                loadingImage.classList.add("d-none");
            }
            console.log('Oh shit...');
            console.error('Error loading avatar type:', error.message);
        }
    }

    function setupAvatarTypeChangeListener() {
        const radioButtons = document.querySelectorAll('input[name="flexRadioDefault"]');
        radioButtons.forEach((radio) => {
            radio.addEventListener('change', async function() {
                if (this.checked) {
                    const newAvatarType = this.value;
                    try {
                        const response = await fetch('/api/editor/type/change', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ avatarType: newAvatarType })
                        });

                        if (!response.ok) {
                            throw new Error('Failed to change avatar type');
                        }

                        await requestReRender();
                    } catch (error) {
                        console.log('Oh shit...');
                        console.error('Error changing avatar type:', error.message);
                    }
                }
            });
        });
    }

    const colorButtonsContainer = document.getElementById('color-buttons-container');

    function getHue(hex) {
        const r = parseInt(hex.substr(1, 2), 16) / 255;
        const g = parseInt(hex.substr(3, 2), 16) / 255;
        const b = parseInt(hex.substr(5, 2), 16) / 255;

        const max = Math.max(r, g, b);
        const min = Math.min(r, g, b);
        let h = 0;
        const l = (max + min) / 2;
        const d = max - min;

        if (d !== 0) {
            if (max === r) {
                h = ((g - b) / d + (g < b ? 6 : 0)) * 60;
            } else if (max === g) {
                h = ((b - r) / d + 2) * 60;
            } else if (max === b) {
                h = ((r - g) / d + 4) * 60;
            }
        }
        return h;
    }

    const sortedColors = Object.entries(brickColorPalette).sort((a, b) => {
        const hueA = getHue(a[1]);
        const hueB = getHue(b[1]);
        return hueA - hueB;
    });

    for (const [brickCode, colorHex] of sortedColors) {
        const brickColorName = brickColorNames[brickCode] || "Unknown";
        const colorButton = document.createElement("button");
        colorButton.classList.add("color-button");
        colorButton.style.backgroundColor = colorHex;
        colorButton.setAttribute('data-bs-dismiss', 'modal');
        colorButton.setAttribute('title', brickColorName);

        colorButton.addEventListener("click", function() {
            if (selectedPartClass) {
                const partElement = document.querySelector(selectedPartClass);
                if (partElement) {
                    partElement.style.backgroundColor = colorHex;
                    partColorMapping[selectedPartClass.substring(1)] = parseInt(brickCode);
                    sendColorUpdate();
                }
            }
        });

        colorButtonsContainer.appendChild(colorButton);
    }

    const bodyParts = document.querySelectorAll('.avatar-colors button');
    bodyParts.forEach(button => {
        button.addEventListener('click', function() {
            selectedPartClass = '.' + button.classList[0];
        });
    });

    async function sendColorUpdate() {
        const colorData = {
            left_arm: partColorMapping["color-block-left-arm"],
            right_arm: partColorMapping["color-block-right-arm"],
            left_leg: partColorMapping["color-block-left-leg"],
            right_leg: partColorMapping["color-block-right-leg"],
            head: partColorMapping["color-block-head"],
            torso: partColorMapping["color-block-torso"]
        };

        try {
            const response = await fetch('/api/editor/bodycolors/colors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(colorData)
            });

            if (!response.ok) {
                throw new Error('Failed to update color');
            }

            await requestReRender();
        } catch (error) {
            console.log('Oh shit...');
            console.error('Error sending color update:', error.message);
        }
    }

    redrawBtn.addEventListener("click", function() {
        if (pressedReDraw) return;

        pressedReDraw = true;
        requestReRender();

        setTimeout(() => {
            pressedReDraw = false;
        }, 6500);
    });

    Promise.all([
        loadAvatarType(),
        setupAvatarTypeChangeListener(),
        loadAvatarBodyColors(),
        loadItems()
    ]).then(() => {
        console.log('All functions started executing!');
    }).catch((error) => {
        console.log('Oh shit...');
        console.error('An error occurred while starting the functions:', error);
    });

    console.log('AVATAR EDITOR LOADED!');
});
