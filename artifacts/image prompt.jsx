import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Palette, Eye, Sparkles, Wand2, Copy, Check } from 'lucide-react';

const ImagePromptTaxonomy = () => {
  const [expandedCategories, setExpandedCategories] = useState({});
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedTheme, setSelectedTheme] = useState(null);
  const [showThemes, setShowThemes] = useState(false);
  const [showGenerator, setShowGenerator] = useState(false);
  const [generatorState, setGeneratorState] = useState({
    category: null,
    subcategory: null,
    themes: [],
    subject: '',
    generatedPrompt: '',
    generatedJSON: null
  });
  const [copied, setCopied] = useState(false);
  const [outputFormat, setOutputFormat] = useState('text'); // 'text' or 'json'

  const thematicElements = {
    "Light & Atmosphere": {
      icon: "☀️",
      description: "How illumination, weather, and atmospheric conditions shape mood and visual hierarchy",
      variations: [
        "Golden Hour - warm, directional, long shadows, nostalgic glow",
        "Overcast Diffusion - soft, even, muted colors, contemplative mood",
        "Dramatic Chiaroscuro - high contrast, theatrical, deep shadows, spotlight effect",
        "Volumetric/God Rays - mystical, dust particles, beam penetration, sacred quality",
        "Bioluminescence - otherworldly glow, darkness punctuated by organic light",
        "Neon/Artificial - synthetic color, urban night, reflective surfaces, cyberpunk palette"
      ],
      applications: "Works across all categories - transforms realism into noir, makes fantasy ethereal, gives sci-fi its blade runner aesthetic, shifts portraits from corporate to intimate"
    },
    "Scale & Perspective": {
      icon: "🔭",
      description: "Relationship between subject size, viewer position, and spatial hierarchy",
      variations: [
        "Monumental/Epic - towering subjects, ant's-eye view, sublime vastness, human insignificance",
        "Intimate/Macro - extreme close-up, texture primacy, abstract through proximity",
        "Bird's Eye/Isometric - god view, pattern recognition, strategic distance, map-like",
        "Dutch Angle/Tilted - psychological unease, dynamic energy, instability",
        "Forced Perspective - deliberate scale manipulation, optical illusion, surreal juxtaposition",
        "Deep Space - layered depth, atmospheric perspective, foreground-middle-background clarity"
      ],
      applications: "Essential for architectural work, transforms character portraits, defines fantasy epic vs personal story, makes product photography heroic or approachable"
    },
    "Temporal Quality": {
      icon: "⏳",
      description: "How the image relates to time - frozen moment, duration, decay, or progression",
      variations: [
        "Decisive Moment - peak action frozen, implied before/after, kinetic potential",
        "Long Exposure - motion blur, light trails, temporal compression, dreamy smoothness",
        "Decay/Entropy - weathering, rust, overgrowth, passage of time visible",
        "Timeless/Eternal - removed from temporal markers, archetypal, could be any era",
        "Anachronistic - temporal collision, future tech in past settings, historical remix",
        "Seasonal/Cyclical - specific time markers, harvest, bloom, frost, cultural calendar"
      ],
      applications: "Separates documentary from conceptual photography, ages fantasy into history, makes sci-fi present or distant future, gives still life narrative dimension"
    },
    "Color Psychology": {
      icon: "🎨",
      description: "Palette selection and color relationships driving emotional and symbolic meaning",
      variations: [
        "Monochromatic - single hue variations, tonal unity, minimalist elegance, focused mood",
        "Complementary Contrast - opposite wheel pairs, vibrant tension, visual pop",
        "Analogous Harmony - neighboring hues, natural blending, serene cohesion",
        "Desaturated/Muted - reduced chroma, melancholic, sophisticated, period authenticity",
        "Hyper-Saturated - neon intensity, pop art boldness, candy-colored unreality",
        "Symbolic Palette - culturally coded colors (red=danger/passion, blue=trust/cold, etc.)"
      ],
      applications: "Defines branding illustration, separates horror from fantasy, makes portraits psychological vs documentary, gives period work authenticity"
    },
    "Compositional Tension": {
      icon: "⚖️",
      description: "Balance, asymmetry, and visual weight distribution creating dynamic or stable images",
      variations: [
        "Golden Ratio/Spiral - mathematical harmony, natural balance, classical beauty",
        "Rule of Thirds - accessible balance, photographic standard, dynamic stability",
        "Central Symmetry - formal power, religious iconography, authoritative presence",
        "Diagonal Dynamics - movement implication, baroque energy, action emphasis",
        "Negative Space Dominance - breathing room, minimalist power, subject isolation",
        "Chaotic/All-Over - horror vacui, overwhelming detail, no rest areas, anxiety"
      ],
      applications: "Critical for editorial impact, defines action vs contemplative scenes, makes abstract readable, gives product shots their visual strategy"
    },
    "Material & Texture": {
      icon: "🧱",
      description: "Surface qualities and tactile information that add sensory dimension",
      variations: [
        "Organic/Natural - wood grain, stone, fabric weave, biological irregularity",
        "Industrial/Manufactured - metal sheen, plastic smoothness, glass reflectivity, precision",
        "Weathered/Patina - age evidence, wear patterns, historical accumulation",
        "Ethereal/Translucent - gossamer, fog, glass, light diffusion, immateriality",
        "Visceral/Wet - blood, slime, water droplets, uncomfortable tactility",
        "Synthetic/Digital - pixel perfect, screen glow, holographic, impossibly clean"
      ],
      applications: "Distinguishes illustration approaches, gives 3D renders believability, makes fantasy worlds tangible, separates clean corporate from gritty realism"
    },
    "Narrative Density": {
      icon: "📖",
      description: "Amount of storytelling information and implied context within the frame",
      variations: [
        "Environmental Storytelling - background clues, world-building details, no explicit narrative",
        "Single Subject Focus - minimal context, iconic isolation, poster simplicity",
        "Layered Complexity - multiple story threads, foreground/background interplay, rewatch value",
        "Symbolic Condensation - metaphorical objects, allegorical arrangement, conceptual density",
        "Before/After Implication - outcome visible, cause suggested, temporal narrative",
        "Ambiguous Mystery - incomplete information, viewer interpretation required, lynchian"
      ],
      applications: "Separates concept art from portfolio pieces, makes portraits character studies vs beauty shots, defines editorial vs decorative illustration"
    }
  };

  const taxonomy = {
    "Fine Art Movements": {
      icon: "🎨",
      description: "Historical and contemporary art movements with distinct visual languages",
      subcategories: {
        "Classical & Academic": {
          themes: "Idealized beauty, mythological narratives, technical mastery",
          styles: "Precise draftsmanship, balanced composition, naturalistic rendering",
          subjects: "Historical scenes, portraits, religious themes, allegorical figures",
          artists: "Caravaggio, Rembrandt, Vermeer, Bouguereau",
          aesthetics: "Chiaroscuro lighting, sfumato blending, golden ratio composition, oil painting texture"
        },
        "Impressionism & Post-Impressionism": {
          themes: "Light effects, fleeting moments, everyday life, perception",
          styles: "Visible brushwork, vibrant color, broken color technique, outdoor scenes",
          subjects: "Landscapes, urban scenes, leisure activities, still life",
          artists: "Monet, Renoir, Van Gogh, Cézanne, Seurat",
          aesthetics: "Dappled light, loose brushstrokes, complementary colors, atmospheric perspective"
        },
        "Modernism & Abstraction": {
          themes: "Form over function, emotional expression, geometric reduction, color theory",
          styles: "Non-representational, geometric abstraction, expressionist distortion",
          subjects: "Pure form, color fields, emotional states, deconstructed reality",
          artists: "Kandinsky, Mondrian, Rothko, Pollock, Malevich",
          aesthetics: "Hard edges, color blocking, gestural marks, spatial ambiguity, minimal palettes"
        },
        "Surrealism & Symbolism": {
          themes: "Dreams, unconscious mind, symbolic meaning, psychological depth",
          styles: "Hyper-realistic rendering of impossible scenarios, symbolic imagery",
          subjects: "Dream landscapes, metamorphosis, juxtaposition, archetypal symbols",
          artists: "Dalí, Magritte, Ernst, Moreau, Redon",
          aesthetics: "Photorealistic technique with impossible content, visual paradox, uncanny valley"
        },
        "Expressionism & Fauvism": {
          themes: "Raw emotion, subjective experience, psychological intensity, primal feeling",
          styles: "Bold distortion, exaggerated form, emotional color, aggressive brushwork",
          subjects: "Tortured figures, urban anxiety, psychological portraits, emotional landscapes",
          artists: "Munch, Kirchner, Matisse, Derain, Nolde",
          aesthetics: "Non-naturalistic color, angular forms, thick impasto, expressive line quality"
        },
        "Cubism & Geometric Deconstruction": {
          themes: "Multiple perspectives, analytical fragmentation, spatial ambiguity, simultaneous views",
          styles: "Fragmented planes, geometric reduction, monochromatic palettes, collage elements",
          subjects: "Still life dissection, portrait faceting, architectural analysis, object studies",
          artists: "Picasso, Braque, Gris, Léger, Delaunay",
          aesthetics: "Overlapping planes, muted earth tones, newspaper collage, shallow pictorial space"
        },
        "Art Nouveau & Decorative Arts": {
          themes: "Natural forms, organic flow, ornamental elegance, craft elevation",
          styles: "Sinuous curves, botanical motifs, flat decorative patterns, asymmetric composition",
          subjects: "Feminine figures, floral patterns, architectural ornament, poster design",
          artists: "Mucha, Klimt, Beardsley, Tiffany, Horta",
          aesthetics: "Whiplash curves, gold leaf accents, stained glass color, japonisme influence"
        },
        "Social Realism & Ashcan School": {
          themes: "Working class dignity, social critique, urban reality, political consciousness",
          styles: "Direct observation, unglamorous subjects, documentary approach, muted palettes",
          subjects: "Factory workers, tenement life, labor struggles, street scenes",
          artists: "Diego Rivera, Käthe Kollwitz, George Bellows, Ben Shahn",
          aesthetics: "Gritty textures, somber tones, compositional drama, humanist focus"
        },
        "Baroque & Dramatic Naturalism": {
          themes: "Theatrical grandeur, emotional intensity, religious ecstasy, power dynamics",
          styles: "Dynamic composition, dramatic lighting, movement emphasis, illusionistic space",
          subjects: "Religious martyrdom, mythological drama, aristocratic portraits, allegorical ceilings",
          artists: "Rubens, Bernini, Artemisia Gentileschi, Velázquez",
          aesthetics: "Tenebrism, diagonal thrust, foreshortening, rich fabric textures, theatrical gestures"
        }
      }
    },
    "Contemporary Digital Styles": {
      icon: "💻",
      description: "Modern digital art aesthetics and techniques enabled by technology",
      subcategories: {
        "Hyperrealism & Photobashing": {
          themes: "Extreme detail, technical virtuosity, believable impossibilities",
          styles: "Photo-manipulation, 3D integration, matte painting techniques",
          subjects: "Fantasy landscapes, product visualization, concept vehicles, architectural renders",
          artists: "Beeple, Maciej Kuciara, Eytan Zana",
          aesthetics: "8K resolution detail, physically-based rendering, atmospheric scattering, HDR lighting"
        },
        "Flat Design & Vector Art": {
          themes: "Clarity, simplicity, geometric reduction, brand-friendly aesthetics",
          styles: "Solid colors, minimal shading, geometric shapes, clean lines",
          subjects: "Icons, infographics, character design, editorial illustration",
          artists: "Malika Favre, Tom Haugomat, DKNG Studios",
          aesthetics: "Limited palette, negative space, geometric primitives, layered transparency"
        },
        "Cyberpunk & Neon Aesthetics": {
          themes: "High-tech/low-life, corporate dystopia, urban decay, technological sublime",
          styles: "Neon lighting, rain-slicked surfaces, holographic interfaces, gritty realism",
          subjects: "Megacities, cyborgs, street scenes, corporate towers, underground markets",
          artists: "Simon Stålenhag, Maciej Rebisz, Liam Wong",
          aesthetics: "Neon glow, chromatic aberration, volumetric lighting, wet reflections, purple-cyan palette"
        },
        "Low Poly & Isometric": {
          themes: "Playful abstraction, game-ready aesthetics, accessible complexity",
          styles: "Faceted geometry, flat shading, axonometric projection",
          subjects: "Architectural scenes, game environments, tech illustrations, infographic worlds",
          artists: "Timothy J. Reynolds, Matt Anderson, Peter Tarka",
          aesthetics: "Triangulated meshes, bold colors, no gradients, 30° isometric angle, ambient occlusion"
        },
        "Glitch Art & Datamoshing": {
          themes: "Digital decay, technological aesthetics, corrupted beauty, system failure as art",
          styles: "Pixel sorting, compression artifacts, RGB channel separation, databending",
          subjects: "Corrupted portraits, digital landscapes, abstract glitch patterns, error aesthetics",
          artists: "Rosa Menkman, Phillip Stearns, Sabato Visconti",
          aesthetics: "Scan lines, pixelation, color channel shifts, compression blocks, digital noise"
        },
        "Vaporwave & Retrowave": {
          themes: "80s/90s nostalgia, consumerist critique, digital utopia, retrofuturism",
          styles: "Pastel gradients, grid patterns, retro 3D primitives, VHS aesthetics",
          subjects: "Classical statues with tech, sunset grids, palm trees, Japanese text, consumer products",
          artists: "Vektroid aesthetic, James White, Signalnoise",
          aesthetics: "Pink-purple gradients, grid floors, chrome surfaces, VHS scanlines, palm tree silhouettes"
        },
        "AI-Assisted Surrealism": {
          themes: "Machine dreams, latent space exploration, prompt-driven chaos, emergent aesthetics",
          styles: "Diffusion artifacts, training data echoes, neural network hallucinations, hybrid forms",
          subjects: "Impossible anatomies, merged concepts, style transfer experiments, prompt literalism",
          artists: "Mario Klingemann, Refik Anadol, Sofia Crespo",
          aesthetics: "Soft focus blend, anatomical inconsistencies, texture bleeding, oversaturation, uncanny details"
        },
        "Maximalist Digital Collage": {
          themes: "Information overload, cultural remix, chaotic abundance, digital baroque",
          styles: "Layer stacking, extreme density, source variety, compositional chaos",
          subjects: "Pop culture mashups, political commentary, consumer critique, internet aesthetics",
          artists: "Filip Hodas, Billelis, Ash Thorp",
          aesthetics: "High saturation, overlapping elements, texture variety, depth through layering, visual noise"
        },
        "Minimalist 3D & Clean Renders": {
          themes: "Pure form, material study, spatial serenity, architectural precision",
          styles: "Single light sources, gradient backgrounds, material focus, simple composition",
          subjects: "Abstract forms, product studies, architectural elements, material explorations",
          artists: "Peter Tarka, Ari Weinkle, Alexis Christodoulou",
          aesthetics: "Soft shadows, pastel palettes, reflective surfaces, ambient light, geometric purity"
        }
      }
    },
    "Illustration Traditions": {
      icon: "✏️",
      description: "Narrative-driven visual communication across media and eras",
      subcategories: {
        "Children's Book Illustration": {
          themes: "Wonder, imagination, accessibility, emotional warmth",
          styles: "Varied from watercolor to digital, emphasis on character and readability",
          subjects: "Fantastical creatures, anthropomorphic animals, child protagonists, magical worlds",
          artists: "Beatrix Potter, Maurice Sendak, Shaun Tan, Oliver Jeffers",
          aesthetics: "Soft edges, expressive characters, limited palette, textural media, clear silhouettes"
        },
        "Editorial & Political Illustration": {
          themes: "Social commentary, satire, conceptual metaphor, visual argumentation",
          styles: "Conceptual clarity, symbolic imagery, varied from minimalist to detailed",
          subjects: "Political figures, social issues, economic concepts, cultural phenomena",
          artists: "Brad Holland, Anita Kunz, Christoph Niemann, Steve Brodner",
          aesthetics: "Visual metaphor, bold composition, cultural iconography, editorial wit"
        },
        "Comic & Sequential Art": {
          themes: "Narrative flow, dynamic action, character expression, visual storytelling",
          styles: "Panel composition, line art dominance, visual rhythm, reading flow",
          subjects: "Superheroes, slice-of-life, science fiction, fantasy epics, memoir",
          artists: "Moebius, Jack Kirby, Naoki Urasawa, Fiona Staples",
          aesthetics: "Dynamic angles, speed lines, emanata, gutters, speech balloons, ink hatching"
        },
        "Botanical & Scientific Illustration": {
          themes: "Accuracy, educational clarity, aesthetic precision, documentary beauty",
          styles: "Detailed rendering, taxonomic accuracy, neutral backgrounds",
          subjects: "Flora, fauna, anatomical studies, astronomical diagrams, geological specimens",
          artists: "Maria Sibylla Merian, Ernst Haeckel, John James Audubon",
          aesthetics: "Precise linework, labeled diagrams, watercolor transparency, white backgrounds"
        },
        "Golden Age Illustration": {
          themes: "Romantic adventure, classical beauty, narrative drama, commercial artistry",
          styles: "Oil painting techniques, dramatic lighting, figure-focused composition",
          subjects: "Literary scenes, adventure narratives, romantic encounters, historical tableaus",
          artists: "N.C. Wyeth, Howard Pyle, J.C. Leyendecker, Norman Rockwell",
          aesthetics: "Rich oil glazes, heroic poses, period costumes, theatrical lighting, saturated color"
        },
        "Manga & Anime Aesthetics": {
          themes: "Emotional extremes, stylized beauty, action intensity, youth culture",
          styles: "Large expressive eyes, speed lines, screen tone patterns, simplified backgrounds",
          subjects: "School life, mecha battles, romantic drama, supernatural adventures",
          artists: "Osamu Tezuka, Hayao Miyazaki, Katsuhiro Otomo, CLAMP",
          aesthetics: "Sharp ink lines, screen tone gradients, sparkle effects, exaggerated expressions, minimal color"
        },
        "Woodcut & Printmaking Traditions": {
          themes: "Folk narrative, social messaging, craft authenticity, graphic boldness",
          styles: "High contrast, carved line quality, limited colors, registration marks",
          subjects: "Folk tales, political posters, nature studies, religious imagery",
          artists: "Albrecht Dürer, Hokusai, Käthe Kollwitz, Yoshitoshi",
          aesthetics: "Wood grain texture, bold black lines, flat color areas, visible registration, paper texture"
        },
        "Fashion Illustration": {
          themes: "Elegance, trend documentation, aspirational beauty, textile focus",
          styles: "Elongated figures, fabric rendering, loose gestural quality, color emphasis",
          subjects: "Runway looks, accessory details, textile patterns, idealized figures",
          artists: "René Gruau, Antonio Lopez, David Downton, Mats Gustafson",
          aesthetics: "Flowing lines, selective detail, fashion proportion, watercolor washes, ink confidence"
        },
        "Vintage Travel Poster": {
          themes: "Destination romance, modernist optimism, simplified iconography, wanderlust",
          styles: "Flat color, simplified forms, bold typography integration, streamlined composition",
          subjects: "Landmarks, transportation, exotic locales, leisure activities",
          artists: "A.M. Cassandre, Roger Broders, Tom Purvis, Leslie Ragan",
          aesthetics: "Art Deco geometry, limited palette, airbrushed gradients, bold sans-serif type, heroic scale"
        }
      }
    },
    "Photography Genres": {
      icon: "📷",
      description: "Photographic approaches and their characteristic visual qualities",
      subcategories: {
        "Portrait & Fashion": {
          themes: "Human expression, identity, beauty standards, personal narrative",
          styles: "Studio lighting, environmental portraits, candid moments, editorial staging",
          subjects: "Individuals, groups, fashion editorials, character studies",
          artists: "Annie Leibovitz, Richard Avedon, Cindy Sherman, Irving Penn",
          aesthetics: "Shallow depth of field, catch lights, rim lighting, color grading, posed vs candid"
        },
        "Landscape & Nature": {
          themes: "Sublime wilderness, environmental awareness, seasonal change, scale",
          styles: "Golden hour lighting, long exposure, aerial perspective, macro detail",
          subjects: "Mountains, forests, seascapes, wildlife, weather phenomena, celestial events",
          artists: "Ansel Adams, Sebastião Salgado, Frans Lanting, Michael Kenna",
          aesthetics: "Deep focus, graduated filters, HDR blending, foreground interest, rule of thirds"
        },
        "Street & Documentary": {
          themes: "Decisive moments, social observation, urban life, unposed reality",
          styles: "Available light, grab shots, layered composition, geometric framing",
          subjects: "Urban scenes, cultural events, everyday life, social conditions",
          artists: "Henri Cartier-Bresson, Vivian Maier, Fan Ho, Joel Meyerowitz",
          aesthetics: "Grainy film, high contrast B&W, dynamic composition, human scale, candid expression"
        },
        "Architectural & Interior": {
          themes: "Spatial experience, design documentation, geometric beauty, built environment",
          styles: "Perspective correction, symmetrical framing, detail shots, ambient lighting",
          subjects: "Buildings, interiors, urban planning, structural details, spatial relationships",
          artists: "Julius Shulman, Iwan Baan, Candida Höfer, Andreas Gursky",
          aesthetics: "Tilt-shift correction, leading lines, symmetry, vanishing points, material texture"
        },
        "Fine Art & Conceptual": {
          themes: "Artistic vision, conceptual exploration, staged narratives, photographic sculpture",
          styles: "Constructed scenes, studio control, symbolic imagery, experimental techniques",
          subjects: "Staged tableaus, symbolic objects, constructed realities, photographic essays",
          artists: "Gregory Crewdson, Jeff Wall, Hiroshi Sugimoto, Sally Mann",
          aesthetics: "Cinematic lighting, meticulous staging, large format detail, theatrical composition, timeless quality"
        },
        "Aerial & Drone Photography": {
          themes: "Pattern recognition, abstract landscapes, environmental overview, unique perspective",
          styles: "Top-down composition, geometric abstraction, scale revelation, environmental patterns",
          subjects: "Agricultural patterns, urban grids, natural formations, infrastructure networks",
          artists: "Yann Arthus-Bertrand, Alex MacLean, Bernhard Lang",
          aesthetics: "Flattened perspective, geometric patterns, color field abstraction, texture emphasis, minimal horizon"
        },
        "Astrophotography & Night Sky": {
          themes: "Cosmic scale, temporal duration, light pollution contrast, celestial wonder",
          styles: "Long exposure, star trails, light painting, composite stacking",
          subjects: "Milky Way, star trails, aurora, deep sky objects, planetary detail",
          artists: "Michael Shainblum, Babak Tafreshi, Royce Bair",
          aesthetics: "Star point sharpness, light pollution gradients, foreground silhouettes, deep space color, time-lapse blur"
        },
        "High-Speed & Motion": {
          themes: "Frozen motion, temporal precision, kinetic energy, invisible moments",
          styles: "Flash sync, bullet time, motion blur contrast, split-second timing",
          subjects: "Water splashes, bullet impacts, athletic peak moments, breaking objects",
          artists: "Harold Edgerton, Stephen Dalton, Philippe Halsman",
          aesthetics: "Sharp freeze, motion trails, suspended liquids, peak action, impossible detail, strobe artifacts"
        },
        "Analog & Film Photography": {
          themes: "Material authenticity, chemical process, grain aesthetic, slow photography",
          styles: "Film grain, light leaks, color shifts, physical manipulation",
          subjects: "Universal subjects with analog character, tactile documentation, nostalgic moods",
          artists: "William Eggleston, Saul Leiter, Nan Goldin, Stephen Shore",
          aesthetics: "Visible grain, color saturation shifts, vignetting, light leaks, Kodachrome palette, silver gelatin tones"
        }
      }
    },
    "Genre & Thematic Categories": {
      icon: "🎭",
      description: "Subject-matter driven approaches transcending medium or style",
      subcategories: {
        "Fantasy & Mythology": {
          themes: "Epic narratives, archetypal heroes, magical systems, world-building",
          styles: "Detailed environments, dramatic lighting, costume design, creature anatomy",
          subjects: "Dragons, wizards, enchanted forests, ancient civilizations, magical artifacts",
          artists: "Frank Frazetta, Brian Froud, Alan Lee, Yoshitaka Amano",
          aesthetics: "Atmospheric perspective, rim lighting, ornate detail, scale contrast, mystical glow"
        },
        "Science Fiction & Futurism": {
          themes: "Technological speculation, space exploration, alien worlds, societal evolution",
          styles: "Hard-surface design, functional aesthetics, environmental storytelling",
          subjects: "Spacecraft, alien landscapes, futuristic cities, robots, space stations",
          artists: "Syd Mead, Chris Foss, John Harris, Sparth",
          aesthetics: "Clean geometry, metallic surfaces, lens flares, scale megastructures, cockpit POV"
        },
        "Horror & Dark Fantasy": {
          themes: "Fear, the uncanny, body horror, psychological dread, gothic atmosphere",
          styles: "Desaturated palettes, dramatic shadows, unsettling composition, visceral detail",
          subjects: "Monsters, haunted spaces, psychological distortion, occult imagery, decay",
          artists: "Zdzisław Beksiński, H.R. Giger, Junji Ito, Simon Bisley",
          aesthetics: "Chiaroscuro extremes, organic-mechanical fusion, Dutch angles, fog/mist, elongation"
        },
        "Historical & Period": {
          themes: "Authenticity, cultural specificity, temporal atmosphere, documentary accuracy",
          styles: "Period-accurate detail, historical research, costume accuracy, architectural fidelity",
          subjects: "Historical events, period costumes, architectural landmarks, cultural practices",
          artists: "Howard Pyle, N.C. Wyeth, James Gurney, Angus McBride",
          aesthetics: "Natural materials, period lighting, authentic color palettes, historical composition"
        },
        "Steampunk & Alternative History": {
          themes: "Victorian retrofuturism, industrial romance, anachronistic technology, brass aesthetics",
          styles: "Mechanical detail, Victorian ornamentation, industrial materials, gear mechanisms",
          subjects: "Airships, clockwork devices, steam machinery, alternative Victorian worlds",
          artists: "Ian McQue, Jakub Rozalski, Keith Thompson",
          aesthetics: "Brass and copper tones, visible gears, steam effects, riveted plates, ornate Victorian detail"
        },
        "Post-Apocalyptic & Wasteland": {
          themes: "Civilizational collapse, resource scarcity, survival aesthetics, environmental ruin",
          styles: "Weathered textures, scavenged assemblage, harsh lighting, desolate composition",
          subjects: "Ruined cities, makeshift settlements, resource conflicts, environmental devastation",
          artists: "Simon Stålenhag, Ian McQue, Feng Zhu",
          aesthetics: "Rust and decay, dust atmosphere, harsh sunlight, improvised tech, sand and grime"
        },
        "Solarpunk & Eco-Futurism": {
          themes: "Environmental harmony, renewable futures, optimistic speculation, nature-tech integration",
          styles: "Organic architecture, green integration, bright palettes, community focus",
          subjects: "Vertical gardens, solar infrastructure, public transit, sustainable cities, bio-architecture",
          artists: "Luc Schuiten, Vincent Callebaut, various concept artists",
          aesthetics: "Abundant greenery, solar panel integration, warm natural light, flowing organic forms, vibrant plant life"
        },
        "Urban Fantasy & Magical Realism": {
          themes: "Magic in modernity, hidden worlds, supernatural coexistence, wonder in the mundane",
          styles: "Realistic base with fantastical elements, subtle magic, contemporary settings",
          subjects: "Modern cities with magic, supernatural creatures in crowds, hidden realms, everyday enchantment",
          artists: "Wylie Beckert, Victo Ngai, Karla Ortiz",
          aesthetics: "Realistic lighting with magical accents, contemporary detail, subtle glows, urban textures with ethereal overlays"
        },
        "Afrofuturism & Cultural Futurism": {
          themes: "Cultural heritage meets technology, diaspora futures, ancestral knowledge, speculative identity",
          styles: "Traditional pattern integration, vibrant color, technological fusion, cultural symbolism",
          subjects: "Futuristic African cities, technological adornment, ancestral tech, cultural celebration",
          artists: "Osborne Macharia, Ashley A. Woods, John Jennings",
          aesthetics: "Bold patterns, rich jewel tones, metallic accents, cultural textile integration, dynamic composition"
        }
      }
    },
    "Rendering Techniques": {
      icon: "🖌️",
      description: "Medium-specific execution methods and their characteristic qualities",
      subcategories: {
        "Traditional Media": {
          themes: "Physical texture, material authenticity, artistic gesture, medium limitations",
          styles: "Visible brushwork, paper texture, pigment behavior, blending techniques",
          subjects: "Universal - technique defines aesthetic more than subject",
          artists: "Medium-specific: Sargent (oil), Winslow Homer (watercolor), Degas (pastel)",
          aesthetics: "Canvas texture, paint thickness, water blooms, charcoal smudging, ink bleeding"
        },
        "3D & CGI": {
          themes: "Mathematical precision, material simulation, lighting accuracy, impossible camera",
          styles: "Ray-traced lighting, subsurface scattering, procedural generation, physics simulation",
          subjects: "Product renders, architectural viz, character models, VFX integration",
          artists: "Ian Hubert, Ash Thorp, Beeple, Cornelius Dämmrich",
          aesthetics: "Perfect reflections, global illumination, depth of field, motion blur, caustics"
        },
        "Mixed Media & Collage": {
          themes: "Juxtaposition, layering, textural variety, conceptual combination",
          styles: "Cut-and-paste aesthetics, transparency overlays, textural contrast",
          subjects: "Conceptual compositions, surreal combinations, deconstructed imagery",
          artists: "Hannah Höch, Romare Bearden, Kara Walker, Wangechi Mutu",
          aesthetics: "Visible edges, layer blending, texture overlay, scale manipulation, source variety"
        },
        "Generative & Algorithmic": {
          themes: "Mathematical beauty, emergent complexity, parametric variation, system aesthetics",
          styles: "Fractal patterns, particle systems, cellular automata, noise functions",
          subjects: "Abstract patterns, data visualization, procedural landscapes, algorithmic portraits",
          artists: "Manfred Mohr, Casey Reas, Tyler Hobbs, Anna Ridler",
          aesthetics: "Perfect repetition with variation, mathematical curves, RGB precision, grid systems"
        },
        "Ink & Line Art": {
          themes: "Graphic clarity, linear expression, monochromatic boldness, technique mastery",
          styles: "Hatching, cross-hatching, stippling, contour variation, brush calligraphy",
          subjects: "Figure studies, architectural rendering, comic art, botanical detail",
          artists: "Franklin Booth, Charles Dana Gibson, Kim Jung Gi, Bernie Wrightson",
          aesthetics: "Line weight variation, pen texture, spot blacks, white space usage, hatching density"
        },
        "Spray Paint & Graffiti Techniques": {
          themes: "Urban expression, can control, layered stencils, street aesthetics",
          styles: "Spray gradients, drip effects, stencil precision, tag calligraphy, quick execution",
          subjects: "Street murals, character work, abstract pieces, political messages",
          artists: "Banksy, Futura 2000, Lady Pink, Os Gemeos",
          aesthetics: "Spray fade, drip marks, stencil edges, cap variation, aerosol texture, urban patina"
        },
        "Digital Painting & Matte Painting": {
          themes: "Photorealistic environments, concept visualization, seamless integration, impossible realities",
          styles: "Brush simulation, photo integration, atmospheric depth, texture building",
          subjects: "Concept environments, VFX backgrounds, fantasy landscapes, sci-fi cities",
          artists: "Craig Mullins, Dylan Cole, Feng Zhu, Raphael Lacoste",
          aesthetics: "Photographic detail, atmospheric perspective, texture variety, seamless blending, painted-photo hybrid"
        },
        "Textile & Fiber Arts": {
          themes: "Material warmth, craft tradition, tactile richness, pattern repetition",
          styles: "Woven texture, embroidered detail, quilted layers, fiber manipulation",
          subjects: "Tapestries, quilts, fiber sculptures, textile patterns, wearable art",
          artists: "Faith Ringgold, Sheila Hicks, Jeffrey Gibson, Bisa Butler",
          aesthetics: "Thread texture, fabric drape, stitching patterns, fiber density, material layering, textile grain"
        },
        "Pixel Art & Retro Gaming": {
          themes: "Constraint creativity, nostalgia, grid precision, color limitation",
          styles: "Dithering, limited palette, tile repetition, sprite clarity, anti-aliasing techniques",
          subjects: "Game characters, retro scenes, limited color landscapes, icon design",
          artists: "Paul Robertson, eBoy, Waneella, Toyoi Yuuta",
          aesthetics: "Visible pixels, dithering patterns, limited color palettes, tile grids, CRT scanline simulation"
        }
      }
    }
  };

  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  const selectCategory = (mainCat, subCat) => {
    setSelectedCategory({ main: mainCat, sub: subCat });
  };

  const toggleThemeSelection = (themeName) => {
    setGeneratorState(prev => ({
      ...prev,
      themes: prev.themes.includes(themeName)
        ? prev.themes.filter(t => t !== themeName)
        : [...prev.themes, themeName]
    }));
  };

  const generatePrompt = () => {
    const { category, subcategory, themes, subject } = generatorState;
    
    if (!category || !subcategory || !subject) {
      setGeneratorState(prev => ({ 
        ...prev, 
        generatedPrompt: 'Please select a category, subcategory, and enter a subject.',
        generatedJSON: null
      }));
      return;
    }

    const subData = taxonomy[category].subcategories[subcategory];
    
    // === NEW: SUBJECT INTERPRETATION ===
    // Expand generic subjects into specific visual descriptions
    const interpretSubject = (rawSubject) => {
      const subject = rawSubject.toLowerCase().trim();
      
      // Pattern matching for common generic inputs
      const interpretations = {
        // People descriptions
        'beautiful italian woman': 'A young Italian woman with olive skin, dark expressive eyes, flowing black hair, wearing elegant period clothing. She stands in three-quarter pose',
        'beautiful woman': 'A woman with refined features, expressive eyes, elegant posture, and flowing hair. Captured in natural light',
        'old man': 'An elderly man with weathered skin, deep-set eyes, silver hair, and contemplative expression. Character lines tell stories of age',
        'child': 'A young child with innocent expression, bright curious eyes, soft features. Captured in a moment of wonder',
        'warrior': 'A battle-hardened warrior in detailed armor, weathered equipment, strong stance, determined expression. Scars and experience visible',
        
        // Places
        'forest': 'A dense woodland with towering trees, dappled sunlight filtering through canopy, moss-covered ground, atmospheric depth',
        'city': 'An urban landscape with layered architecture, street-level detail, distant buildings creating depth, human activity',
        'mountain': 'A dramatic mountain peak with rocky crags, snow-capped summit, atmospheric distance, scale emphasized by foreground elements',
        'beach': 'A coastal scene with textured sand, rolling waves, horizon line, sky reflecting on wet surfaces',
        'desert': 'An arid landscape with undulating dunes, harsh sunlight casting long shadows, sparse vegetation, heat shimmer atmosphere',
        
        // Objects
        'flower': 'A botanical specimen with delicate petals, visible stamens, subtle color gradations, stem and leaves showing natural growth',
        'building': 'An architectural structure with detailed facade, material textures, geometric forms, relationship to surrounding space',
        'car': 'A vehicle with sleek body lines, reflective surfaces, wheel detail, positioned to show form and character',
        'book': 'An aged tome with worn leather binding, visible page edges, embossed cover detail, positioned to show depth',
        
        // Abstract concepts
        'love': 'Two figures in intimate proximity, tender gestures, soft lighting, emotional connection visible through body language',
        'war': 'A battlefield scene with conflict dynamics, dramatic lighting, scattered equipment, atmospheric smoke and chaos',
        'death': 'Symbolic imagery of mortality - skeletal forms, wilting organic matter, extinguished light sources, temporal decay',
        'time': 'Temporal symbols - clockwork mechanisms, aging subjects, seasonal transitions, light quality suggesting passage',
        'dream': 'Surreal juxtapositions, floating elements defying gravity, impossible architecture, soft focus transitions',
        
        // Actions
        'running': 'A figure captured mid-stride, dynamic pose showing motion, clothing and hair suggesting movement, forward momentum',
        'dancing': 'A dancer in expressive pose, body showing fluid motion, fabric in movement, grace and energy captured',
        'fighting': 'Combatants in dynamic action, weapons or fists mid-strike, muscular tension visible, spatial conflict',
        'sleeping': 'A resting figure in peaceful repose, relaxed body language, soft ambient light, quiet atmosphere'
      };
      
      // Check for exact matches first
      if (interpretations[subject]) {
        return interpretations[subject];
      }
      
      // Pattern matching for partial matches
      if (subject.includes('woman') || subject.includes('female')) {
        const descriptors = subject.split(' ').filter(w => !['woman', 'female', 'a', 'an', 'the'].includes(w));
        return `A woman with ${descriptors.join(' ')} characteristics, expressive features, natural posture. Details emphasize ${descriptors[0] || 'unique'} qualities`;
      }
      
      if (subject.includes('man') || subject.includes('male')) {
        const descriptors = subject.split(' ').filter(w => !['man', 'male', 'a', 'an', 'the'].includes(w));
        return `A man with ${descriptors.join(' ')} features, strong presence, characteristic expression. Physical details emphasize ${descriptors[0] || 'masculine'} attributes`;
      }
      
      if (subject.includes('landscape') || subject.includes('scene')) {
        return `A sweeping vista with layered depth, foreground elements providing scale, middle-ground detail, background atmospheric perspective. Environmental narrative through composition`;
      }
      
      if (subject.includes('portrait')) {
        return `A close portrait composition focusing on facial features, expression, character. Lighting sculpts form and reveals personality`;
      }
      
      if (subject.includes('abstract')) {
        return `An abstract composition of forms, colors, and spatial relationships. Non-representational elements create visual rhythm and emotional resonance`;
      }
      
      // If no pattern matches, enhance with visual specificity
      const words = subject.split(' ');
      if (words.length <= 2) {
        return `A detailed depiction of ${subject} with emphasis on texture, form, lighting, and spatial context. Visual specificity in material qualities and atmospheric treatment`;
      }
      
      // Return original if complex enough (4+ words likely already descriptive)
      return rawSubject;
    };
    
    const interpretedSubject = interpretSubject(subject);
    
    // Extract multiple aesthetic elements for richer detail
    const aestheticsList = subData.aesthetics.split(',').map(s => s.trim());
    const selectedAesthetics = aestheticsList.slice(0, 4).join(', ');
    
    // Get random artist
    const artistsList = subData.artists.split(',').map(s => s.trim());
    const selectedArtist = artistsList[Math.floor(Math.random() * artistsList.length)];
    
    // Extract style details - get first 2 for specificity
    const stylesList = subData.styles.split(',').map(s => s.trim());
    const selectedStyles = stylesList.slice(0, 2).join(', ');
    
    // Build thematic modifiers with FULL descriptions
    let thematicFullDescriptions = [];
    let thematicShortModifiers = [];
    if (themes.length > 0) {
      themes.forEach(themeName => {
        const themeData = thematicElements[themeName];
        const randomVariation = themeData.variations[Math.floor(Math.random() * themeData.variations.length)];
        thematicFullDescriptions.push(randomVariation);
        thematicShortModifiers.push(randomVariation.split(' - ')[0]);
      });
    }
    
    // Text prompt (using ORIGINAL subject for backward compatibility)
    const textPrompt = `${subject}, ${subData.styles.toLowerCase()}, in the style of ${selectedArtist}, ${thematicShortModifiers.join(', ')}, ${selectedAesthetics}`;
    
    // === JSON generation uses INTERPRETED subject ===
    
    // 1. COMPOSITION NOTES - extract spatial/structural guidance
    const compositionTemplates = [
      "centered composition with balanced foreground and background elements",
      "dynamic diagonal composition leading the eye through the frame",
      "rule of thirds placement with negative space emphasis",
      "symmetrical framing with architectural precision",
      "layered depth with clear foreground, midground, and background separation",
      "close-up framing with intimate spatial relationships",
      "wide establishing shot showing environmental context",
      "vertical emphasis with upward perspective",
      "horizontal panoramic orientation emphasizing breadth"
    ];
    const compositionNote = compositionTemplates[Math.floor(Math.random() * compositionTemplates.length)];
    
    // 2. COLOR PALETTE - extract from aesthetics and themes
    const colorPaletteMap = {
      "Impressionism & Post-Impressionism": "vibrant complementary colors, pastel undertones, warm earth tones",
      "Cyberpunk & Neon Aesthetics": "electric pink, cyan blue, deep purple, neon accents",
      "Surrealism & Symbolism": "dreamlike muted tones, unexpected color juxtapositions, symbolic color coding",
      "Expressionism & Fauvism": "non-naturalistic bold primaries, emotional color choices, saturated intensity",
      "Vaporwave & Retrowave": "pink-purple gradients, electric blue, sunset orange, pastel cyan",
      "Classical & Academic": "rich earth tones, warm skin tones, deep shadows, golden highlights",
      "Horror & Dark Fantasy": "desaturated grays, sickly greens, dried blood reds, shadowy blacks",
      "Solarpunk & Eco-Futurism": "verdant greens, sunny yellows, sky blues, natural earth tones",
      "default": "balanced color harmony with intentional palette limitation"
    };
    const colorPalette = colorPaletteMap[subcategory] || colorPaletteMap["default"];
    
    // 3. CONCEPTUAL HOOK - the "big idea" 
    const conceptualHooks = {
      "Surrealism & Symbolism": "visual paradox challenging rational perception",
      "Cubism & Geometric Deconstruction": "simultaneous multiple viewpoints collapsing spatial logic",
      "AI-Assisted Surrealism": "machine dream aesthetic with emergent uncanny details",
      "Glitch Art & Datamoshing": "intentional digital corruption as aesthetic statement",
      "Horror & Dark Fantasy": "psychological unease through visual distortion",
      "Fine Art & Conceptual": "staged narrative tableau with symbolic intent",
      "Urban Fantasy & Magical Realism": "mundane reality infused with subtle magical intervention",
      "Expressionism & Fauvism": "emotional truth over visual accuracy",
      "default": "visual narrative with thematic coherence"
    };
    const conceptualHook = conceptualHooks[subcategory] || conceptualHooks["default"];
    
    // 4. FINISH QUALITY - surface treatment
    const finishQualityMap = {
      "Traditional Media": "visible brushstrokes, canvas texture, layered paint application",
      "3D & CGI": "perfectly smooth renders, mathematically precise surfaces, photorealistic materials",
      "Hyperrealism & Photobashing": "indistinguishable from photography, pixel-level detail",
      "Flat Design & Vector Art": "completely smooth fills, no texture, crisp vector edges",
      "Ink & Line Art": "confident line variation, visible pen texture, controlled hatching",
      "Oil painting": "thick impasto, visible palette knife marks, glazed layers",
      "Watercolor": "transparent washes, paper texture visible, wet-in-wet bleeding",
      "Digital Painting & Matte Painting": "painted-photo hybrid, soft brush blending, texture overlays",
      "Pixel Art & Retro Gaming": "crisp pixel grid, no anti-aliasing, dithering patterns",
      "default": "medium-appropriate surface treatment with technical control"
    };
    const finishQuality = finishQualityMap[subcategory] || finishQualityMap["default"];
    
    // Core visual elements from the category
    const themeDescriptors = subData.themes.split(',').map(s => s.trim()).slice(0, 2);
    
    // Construct NARRATIVE-STYLE prompt_text (like your example)
    // USE INTERPRETED SUBJECT HERE
    let narrativePrompt = `${interpretedSubject}. `;
    
    // Add compositional/spatial description
    narrativePrompt += `Composition: ${compositionNote}. `;
    
    // Add style and artist reference
    narrativePrompt += `${selectedStyles}, style of ${selectedArtist}. `;
    
    // Add thematic qualities with full descriptions
    if (thematicFullDescriptions.length > 0) {
      narrativePrompt += `${thematicFullDescriptions.join('. ')}. `;
    }
    
    // Add conceptual hook
    narrativePrompt += `Conceptually: ${conceptualHook}. `;
    
    // Add finish quality
    narrativePrompt += `Surface treatment: ${finishQuality}. `;
    
    // Add mood/atmosphere as closing
    narrativePrompt += `Mood: ${themeDescriptors.join(', ')}.`;
    
    // Clean up any double periods
    const cleanedPrompt = narrativePrompt.replace(/\.\./g, '.').replace(/\. \./g, '.');
    
    // JSON structure
    const eraMapping = {
      "Fine Art Movements": "Classical & Modern Traditions",
      "Contemporary Digital Styles": "Contemporary Digital",
      "Illustration Traditions": "Narrative & Commercial Art",
      "Photography Genres": "Photographic Modernism",
      "Genre & Thematic Categories": "Thematic & Speculative",
      "Rendering Techniques": "Technical & Material"
    };
    
    const themeMapping = {
      "Classical & Academic": "Identity & Heritage",
      "Impressionism & Post-Impressionism": "Landscape & Light",
      "Modernism & Abstraction": "Abstraction & Concept",
      "Surrealism & Symbolism": "Narrative & Mythology",
      "Expressionism & Fauvism": "Emotional & Visceral",
      "Cubism & Geometric Deconstruction": "Geometric Analysis",
      "Art Nouveau & Decorative Arts": "Ornamental & Organic",
      "Social Realism & Ashcan School": "Social Documentary",
      "Baroque & Dramatic Naturalism": "Theatrical & Grand",
      "Hyperrealism & Photobashing": "Hyperreality & Simulation",
      "Flat Design & Vector Art": "Graphic & Minimal",
      "Cyberpunk & Neon Aesthetics": "Urban Futures",
      "Low Poly & Isometric": "Geometric Reduction",
      "Glitch Art & Datamoshing": "Digital Corruption",
      "Vaporwave & Retrowave": "Nostalgic Digital",
      "AI-Assisted Surrealism": "Algorithmic Dreams",
      "Maximalist Digital Collage": "Digital Baroque",
      "Minimalist 3D & Clean Renders": "Pure Form",
      "Children's Book Illustration": "Wonder & Imagination",
      "Editorial & Political Illustration": "Social Commentary",
      "Comic & Sequential Art": "Sequential Narrative",
      "Botanical & Scientific Illustration": "Natural Documentation",
      "Golden Age Illustration": "Classical Narrative",
      "Manga & Anime Aesthetics": "Japanese Sequential",
      "Woodcut & Printmaking Traditions": "Graphic Relief",
      "Fashion Illustration": "Sartorial Expression",
      "Vintage Travel Poster": "Modernist Tourism",
      "Portrait & Fashion": "Portraiture & Identity",
      "Landscape & Nature": "Landscape & Environment",
      "Street & Documentary": "Documentary Realism",
      "Architectural & Interior": "Space & Structure",
      "Fine Art & Conceptual": "Conceptual Photography",
      "Aerial & Drone Photography": "Aerial Abstraction",
      "Astrophotography & Night Sky": "Celestial Documentation",
      "High-Speed & Motion": "Temporal Freeze",
      "Analog & Film Photography": "Chemical Process",
      "Fantasy & Mythology": "Narrative & Mythology",
      "Science Fiction & Futurism": "Speculative Futures",
      "Horror & Dark Fantasy": "Gothic & Uncanny",
      "Historical & Period": "Historical Authenticity",
      "Steampunk & Alternative History": "Victorian Futurism",
      "Post-Apocalyptic & Wasteland": "Civilizational Decay",
      "Solarpunk & Eco-Futurism": "Ecological Optimism",
      "Urban Fantasy & Magical Realism": "Contemporary Magic",
      "Afrofuturism & Cultural Futurism": "Cultural Speculation",
      "Traditional Media": "Material & Gesture",
      "3D & CGI": "Digital Simulation",
      "Mixed Media & Collage": "Hybrid & Layered",
      "Generative & Algorithmic": "Algorithmic & Parametric",
      "Ink & Line Art": "Linear Expression",
      "Spray Paint & Graffiti Techniques": "Aerosol Urban",
      "Digital Painting & Matte Painting": "Digital Realism",
      "Textile & Fiber Arts": "Fiber & Textile",
      "Pixel Art & Retro Gaming": "Constraint Graphics"
    };
    
    // Generate ID
    const eraShort = category.split(' ')[0].substring(0, 3).toUpperCase();
    const themeShort = (themeMapping[subcategory] || subcategory).split(' ')[0].substring(0, 3).toUpperCase();
    const randomNum = String(Math.floor(Math.random() * 999) + 1).padStart(3, '0');
    const id = `${eraShort}-${themeShort}-${randomNum}`;
    
    // Extract key elements - use INTERPRETED subject for first element
    const keyElements = [
      interpretedSubject.split(',')[0].split('.')[0].trim().substring(0, 50), // First clause, max 50 chars
      selectedStyles.split(',')[0].trim(),
      ...thematicShortModifiers.slice(0, 1),
      aestheticsList[0]
    ].filter(Boolean).slice(0, 4);
    
    // Extract mood from themes - use actual theme descriptors
    const moodDescriptors = themeDescriptors.map(t => t.charAt(0).toUpperCase() + t.slice(1));
    
    const jsonOutput = {
      id: id,
      era: eraMapping[category] || category,
      movement: subcategory,
      theme: themeMapping[subcategory] || "Mixed Theme",
      style_reference: selectedArtist,
      prompt_text: cleanedPrompt,
      composition_notes: compositionNote,
      color_palette: colorPalette,
      conceptual_hook: conceptualHook,
      finish_quality: finishQuality,
      metadata: {
        key_elements: keyElements,
        mood: moodDescriptors.join(', '),
        technical_params: selectedAesthetics
      }
    };
    
    setGeneratorState(prev => ({ 
      ...prev, 
      generatedPrompt: textPrompt,
      generatedJSON: jsonOutput
    }));
  };

  const copyToClipboard = () => {
    const textToCopy = outputFormat === 'json' 
      ? JSON.stringify(generatorState.generatedJSON, null, 2)
      : generatorState.generatedPrompt;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2 flex items-center gap-3">
            <Palette className="text-violet-600" size={40} />
            Image Prompt Taxonomy
          </h1>
          <p className="text-slate-600 text-lg">A structured framework for diverse and effective image generation</p>
          
          <div className="mt-4 flex gap-3">
            <button
              onClick={() => { setShowThemes(false); setShowGenerator(false); setSelectedTheme(null); }}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                !showThemes && !showGenerator
                  ? 'bg-violet-600 text-white' 
                  : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50'
              }`}
            >
              Categories
            </button>
            <button
              onClick={() => { setShowThemes(true); setShowGenerator(false); setSelectedCategory(null); }}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                showThemes && !showGenerator
                  ? 'bg-violet-600 text-white' 
                  : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50'
              }`}
            >
              Thematic Elements
            </button>
            <button
              onClick={() => { setShowGenerator(true); setShowThemes(false); setSelectedCategory(null); setSelectedTheme(null); }}
              className={`px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2 ${
                showGenerator
                  ? 'bg-violet-600 text-white' 
                  : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50'
              }`}
            >
              <Wand2 size={18} />
              Prompt Generator
            </button>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Navigation Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4 sticky top-6">
              <h2 className="font-semibold text-slate-900 mb-4 flex items-center gap-2">
                <Eye size={20} className="text-violet-600" />
                {showGenerator ? 'Prompt Generator' : showThemes ? 'Thematic Elements' : 'Categories'}
              </h2>
              <div className="space-y-2">
                {showGenerator ? (
                  // Generator Navigation
                  <div className="space-y-4">
                    <div>
                      <label className="block text-xs font-medium text-slate-700 mb-2">1. Select Category</label>
                      <select 
                        className="w-full p-2 border border-slate-200 rounded text-sm"
                        value={generatorState.category || ''}
                        onChange={(e) => setGeneratorState(prev => ({ ...prev, category: e.target.value, subcategory: null }))}
                      >
                        <option value="">Choose...</option>
                        {Object.keys(taxonomy).map(cat => (
                          <option key={cat} value={cat}>{cat}</option>
                        ))}
                      </select>
                    </div>
                    
                    {generatorState.category && (
                      <div>
                        <label className="block text-xs font-medium text-slate-700 mb-2">2. Select Subcategory</label>
                        <select 
                          className="w-full p-2 border border-slate-200 rounded text-sm"
                          value={generatorState.subcategory || ''}
                          onChange={(e) => setGeneratorState(prev => ({ ...prev, subcategory: e.target.value }))}
                        >
                          <option value="">Choose...</option>
                          {Object.keys(taxonomy[generatorState.category].subcategories).map(subcat => (
                            <option key={subcat} value={subcat}>{subcat}</option>
                          ))}
                        </select>
                      </div>
                    )}
                    
                    <div>
                      <label className="block text-xs font-medium text-slate-700 mb-2">3. Add Themes (optional)</label>
                      <div className="space-y-1 max-h-48 overflow-y-auto">
                        {Object.keys(thematicElements).map(theme => (
                          <label key={theme} className="flex items-center gap-2 p-2 hover:bg-slate-50 rounded cursor-pointer">
                            <input
                              type="checkbox"
                              checked={generatorState.themes.includes(theme)}
                              onChange={() => toggleThemeSelection(theme)}
                              className="rounded"
                            />
                            <span className="text-xs text-slate-700">{theme}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-xs font-medium text-slate-700 mb-2">4. Enter Subject</label>
                      <input
                        type="text"
                        className="w-full p-2 border border-slate-200 rounded text-sm"
                        placeholder="e.g., ancient library, cyberpunk street"
                        value={generatorState.subject}
                        onChange={(e) => setGeneratorState(prev => ({ ...prev, subject: e.target.value }))}
                      />
                    </div>
                    
                    <button
                      onClick={generatePrompt}
                      className="w-full bg-violet-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-violet-700 transition-colors flex items-center justify-center gap-2"
                    >
                      <Wand2 size={18} />
                      Generate Prompt
                    </button>
                  </div>
                ) : showThemes ? (
                  // Thematic Elements Navigation
                  Object.entries(thematicElements).map(([theme, data]) => (
                    <button
                      key={theme}
                      onClick={() => setSelectedTheme(theme)}
                      className={`w-full flex items-center gap-2 p-2 rounded transition-colors text-left ${
                        selectedTheme === theme
                          ? 'bg-violet-100 text-violet-900'
                          : 'hover:bg-slate-50'
                      }`}
                    >
                      <span className="text-xl">{data.icon}</span>
                      <span className="text-sm font-medium text-slate-700 flex-1">{theme}</span>
                    </button>
                  ))
                ) : (
                  // Category Navigation (existing)
                  Object.entries(taxonomy).map(([category, data]) => (
                    <div key={category}>
                      <button
                        onClick={() => toggleCategory(category)}
                        className="w-full flex items-center gap-2 p-2 rounded hover:bg-slate-50 transition-colors text-left"
                      >
                        {expandedCategories[category] ? 
                          <ChevronDown size={16} className="text-slate-400" /> : 
                          <ChevronRight size={16} className="text-slate-400" />
                        }
                        <span className="text-xl">{data.icon}</span>
                        <span className="text-sm font-medium text-slate-700 flex-1">{category}</span>
                      </button>
                      {expandedCategories[category] && (
                        <div className="ml-8 mt-1 space-y-1">
                          {Object.keys(data.subcategories).map(subcat => (
                            <button
                              key={subcat}
                              onClick={() => selectCategory(category, subcat)}
                              className={`w-full text-left p-2 rounded text-xs transition-colors ${
                                selectedCategory?.main === category && selectedCategory?.sub === subcat
                                  ? 'bg-violet-100 text-violet-900'
                                  : 'hover:bg-slate-50 text-slate-600'
                              }`}
                            >
                              {subcat}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Content Panel */}
          <div className="lg:col-span-2 space-y-6">
            {showGenerator ? (
              // Prompt Generator Display
              <div className="space-y-6">
                {generatorState.generatedPrompt && (
                  <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold text-slate-900 flex items-center gap-2">
                        <Sparkles size={20} className="text-violet-600" />
                        Generated Output
                      </h3>
                      <div className="flex items-center gap-2">
                        <select
                          value={outputFormat}
                          onChange={(e) => setOutputFormat(e.target.value)}
                          className="text-sm border border-slate-200 rounded px-2 py-1"
                        >
                          <option value="text">Text Prompt</option>
                          <option value="json">JSON Format</option>
                        </select>
                        <button
                          onClick={copyToClipboard}
                          className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 rounded text-sm transition-colors"
                        >
                          {copied ? (
                            <>
                              <Check size={16} className="text-green-600" />
                              <span className="text-green-600">Copied!</span>
                            </>
                          ) : (
                            <>
                              <Copy size={16} />
                              Copy
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                    <div className="bg-violet-50 rounded-lg p-4 border border-violet-100">
                      {outputFormat === 'json' ? (
                        <pre className="text-xs text-slate-800 overflow-x-auto font-mono">
{JSON.stringify(generatorState.generatedJSON, null, 2)}
                        </pre>
                      ) : (
                        <p className="text-slate-800 leading-relaxed">{generatorState.generatedPrompt}</p>
                      )}
                    </div>
                  </div>
                )}
                
                <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
                  <h3 className="font-semibold text-slate-900 mb-4">How It Works</h3>
                  <div className="space-y-3 text-sm text-slate-700">
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 rounded-full bg-violet-100 text-violet-600 flex items-center justify-center flex-shrink-0 font-semibold text-xs">1</div>
                      <div>
                        <p className="font-medium text-slate-900">Select Category & Subcategory</p>
                        <p className="text-slate-600">Defines the core visual language and aesthetic approach</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 rounded-full bg-violet-100 text-violet-600 flex items-center justify-center flex-shrink-0 font-semibold text-xs">2</div>
                      <div>
                        <p className="font-medium text-slate-900">Add Thematic Elements (Optional)</p>
                        <p className="text-slate-600">Layer cross-category modifiers for lighting, scale, color, etc.</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 rounded-full bg-violet-100 text-violet-600 flex items-center justify-center flex-shrink-0 font-semibold text-xs">3</div>
                      <div>
                        <p className="font-medium text-slate-900">Enter Your Subject</p>
                        <p className="text-slate-600">The actual content you want to visualize</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 rounded-full bg-violet-100 text-violet-600 flex items-center justify-center flex-shrink-0 font-semibold text-xs">4</div>
                      <div>
                        <p className="font-medium text-slate-900">Generate & Refine</p>
                        <p className="text-slate-600">The system combines styles, artist references, and aesthetic qualities into a structured prompt</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-lg border border-amber-200 p-6">
                  <h3 className="font-semibold text-amber-900 mb-3 flex items-center gap-2">
                    <Sparkles size={18} />
                    Output Formats
                  </h3>
                  
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-amber-900 text-sm mb-1">Text Prompt</h4>
                      <div className="font-mono text-xs bg-white rounded p-2 text-slate-700 border border-amber-100">
                        [Subject] + [Style] + [Artist] + [Themes] + [Aesthetics]
                      </div>
                      <p className="text-xs text-amber-800 mt-1">Direct input for image generation tools</p>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-amber-900 text-sm mb-1">JSON Format</h4>
                      <div className="font-mono text-xs bg-white rounded p-2 text-slate-700 border border-amber-100">
                        {`{ id, era, movement, theme, style_reference,`}<br/>
                        {`  prompt_text, metadata: { key_elements,`}<br/>
                        {`  mood, technical_params } }`}
                      </div>
                      <p className="text-xs text-amber-800 mt-1">Structured format for libraries, databases, and batch processing</p>
                    </div>
                  </div>
                </div>
              </div>
            ) : showThemes ? (
              // Thematic Elements Display
              selectedTheme ? (
                <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
                  <div className="mb-4">
                    <div className="text-sm text-violet-600 font-medium mb-1">
                      Cross-Category Thematic Element
                    </div>
                    <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                      <span className="text-3xl">{thematicElements[selectedTheme].icon}</span>
                      {selectedTheme}
                    </h2>
                  </div>

                  <div className="space-y-4">
                    <div className="bg-violet-50 rounded-lg p-4 border border-violet-100">
                      <h3 className="font-semibold text-violet-900 mb-2 text-sm uppercase tracking-wide">Description</h3>
                      <p className="text-slate-700">{thematicElements[selectedTheme].description}</p>
                    </div>

                    <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
                      <h3 className="font-semibold text-blue-900 mb-3 text-sm uppercase tracking-wide">Variations</h3>
                      <div className="space-y-2">
                        {thematicElements[selectedTheme].variations.map((variation, idx) => (
                          <div key={idx} className="flex items-start gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-blue-400 mt-2 flex-shrink-0"></div>
                            <p className="text-slate-700 text-sm">{variation}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-100">
                      <h3 className="font-semibold text-emerald-900 mb-2 text-sm uppercase tracking-wide">Cross-Category Applications</h3>
                      <p className="text-slate-700">{thematicElements[selectedTheme].applications}</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12 text-center">
                  <Sparkles size={48} className="text-slate-300 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-slate-900 mb-2">Select a Thematic Element</h3>
                  <p className="text-slate-600">Choose an element to see how it applies across multiple categories</p>
                </div>
              )
            ) : (
              // Category Display (existing)
              selectedCategory ? (
                <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
                  <div className="mb-4">
                    <div className="text-sm text-violet-600 font-medium mb-1">
                      {selectedCategory.main}
                    </div>
                    <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                      {selectedCategory.sub}
                    </h2>
                  </div>

                  {(() => {
                    const data = taxonomy[selectedCategory.main].subcategories[selectedCategory.sub];
                    return (
                      <div className="space-y-4">
                        <div className="bg-violet-50 rounded-lg p-4 border border-violet-100">
                          <h3 className="font-semibold text-violet-900 mb-2 text-sm uppercase tracking-wide">Core Themes</h3>
                          <p className="text-slate-700">{data.themes}</p>
                        </div>

                        <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
                          <h3 className="font-semibold text-blue-900 mb-2 text-sm uppercase tracking-wide">Stylistic Approaches</h3>
                          <p className="text-slate-700">{data.styles}</p>
                        </div>

                        <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-100">
                          <h3 className="font-semibold text-emerald-900 mb-2 text-sm uppercase tracking-wide">Subject Matter</h3>
                          <p className="text-slate-700">{data.subjects}</p>
                        </div>

                        <div className="bg-amber-50 rounded-lg p-4 border border-amber-100">
                          <h3 className="font-semibold text-amber-900 mb-2 text-sm uppercase tracking-wide">Reference Artists</h3>
                          <p className="text-slate-700">{data.artists}</p>
                        </div>

                        <div className="bg-rose-50 rounded-lg p-4 border border-rose-100">
                          <h3 className="font-semibold text-rose-900 mb-2 text-sm uppercase tracking-wide flex items-center gap-2">
                            <Sparkles size={16} />
                            Aesthetic Qualities
                          </h3>
                          <p className="text-slate-700">{data.aesthetics}</p>
                        </div>
                      </div>
                    );
                  })()}
                </div>
              ) : (
                <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12 text-center">
                  <Eye size={48} className="text-slate-300 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-slate-900 mb-2">Select a Category</h3>
                  <p className="text-slate-600">Choose a category from the navigation to view detailed taxonomy information</p>
                </div>
              )
            )}

            {/* Overview Cards */}
            {!showThemes && (
              <div className="grid md:grid-cols-2 gap-4">
                {Object.entries(taxonomy).map(([category, data]) => (
                  <div key={category} className="bg-white rounded-lg shadow-sm border border-slate-200 p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start gap-3 mb-2">
                      <span className="text-3xl">{data.icon}</span>
                      <div className="flex-1">
                        <h3 className="font-semibold text-slate-900">{category}</h3>
                        <p className="text-sm text-slate-600 mt-1">{data.description}</p>
                      </div>
                    </div>
                    <div className="text-xs text-slate-500 mt-3">
                      {Object.keys(data.subcategories).length} subcategories
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {showThemes && !selectedTheme && (
              <div className="grid md:grid-cols-2 gap-4">
                {Object.entries(thematicElements).map(([theme, data]) => (
                  <div 
                    key={theme} 
                    onClick={() => setSelectedTheme(theme)}
                    className="bg-white rounded-lg shadow-sm border border-slate-200 p-4 hover:shadow-md transition-shadow cursor-pointer"
                  >
                    <div className="flex items-start gap-3 mb-2">
                      <span className="text-3xl">{data.icon}</span>
                      <div className="flex-1">
                        <h3 className="font-semibold text-slate-900">{theme}</h3>
                        <p className="text-sm text-slate-600 mt-1">{data.description}</p>
                      </div>
                    </div>
                    <div className="text-xs text-slate-500 mt-3">
                      {data.variations.length} variations
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImagePromptTaxonomy;