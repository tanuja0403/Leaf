import React from 'react';

const Result = ({ result }) => {
  const webLinks = [
    'https://en.wikipedia.org/wiki/Pseudosasa_japonica',
    'https://en.wikipedia.org/wiki/Aesculus_chinensis',
    'https://en.wikipedia.org/wiki/Berberis',
    'https://sites.redlands.edu/trees/species-accounts/eastern-redbud/',
    'https://en.wikipedia.org/wiki/Indigofera_tinctoria',
    'https://en.wikipedia.org/wiki/Acer_palmatum',
    'https://en.wikipedia.org/wiki/Lauraceae',
    'http://hort.uconn.edu/detail.php?pid=238',
    'https://en.wikipedia.org/wiki/Cinnamomum_cassia',
    'https://en.wikipedia.org/wiki/Koelreuteria_paniculata',
    'https://en.wikipedia.org/wiki/Holly',
    'https://en.wikipedia.org/wiki/Pittosporum_tobira',
    'https://en.wikipedia.org/wiki/Chimonanthus',
    'https://en.wikipedia.org/wiki/Cinnamomum_camphora',
    'https://en.wikipedia.org/wiki/Viburnum',
    'https://en.wikipedia.org/wiki/Osmanthus_fragrans',
    'https://en.wikipedia.org/wiki/Cedrus_deodara',
    'https://en.wikipedia.org/wiki/Ginkgo_biloba',
    'https://en.wikipedia.org/wiki/Lagerstroemia',
    'https://en.wikipedia.org/wiki/Nerium',
    'https://en.wikipedia.org/wiki/Podocarpus_macrophyllus',
    'https://www.gardenia.net/plant-variety/Prunus-serrulata-Japanese-Flowering-Cherry',
    'https://en.wikipedia.org/wiki/Ligustrum_lucidum',
    'https://en.wikipedia.org/wiki/Toona_sinensis',
    'https://www.britannica.com/plant/peach',
    'https://ieeexplore.ieee.org/document/7294864',
    'https://en.wikipedia.org/wiki/Acer_buergerianum',
    'https://www.finegardening.com/plant/leatherleaf-mahonia-beales-barberry-mahonia-bealei',
    'https://en.wikipedia.org/wiki/Magnolia_grandiflora',
    'https://en.wikipedia.org/wiki/Populus_%C3%97_canadensis',
    'https://en.wikipedia.org/wiki/Liriodendron_chinense',
    'https://en.wikipedia.org/wiki/Tangerine'
  ];

  const commonNames = [
    'pubescent bamboo', 'Chinese horse chestnut', 'Anhui Barberry',
    'Chinese redbud', 'true indigo', 'Japanese maple', 'Nanmu', 'castor aralia',
    'Chinese cinnamon', 'goldenrain tree', 'Big-fruited Holly', 'Japanese cheesewood',
    'wintersweet', 'camphortree', 'Japan Arrowwood', 'sweet osmanthus',
    'deodar', 'ginkgo, maidenhair tree', 'Crape myrtle, Crepe myrtle',
    'oleander', 'yew plum pine', 'Japanese Flowering Cherry', 'Glossy Privet',
    'Chinese Toon', 'peach', 'Ford Woodlotus', 'trident maple',
    'Beales barberry', 'southern magnolia', 'Canadian poplar',
    'Chinese tulip tree', 'tangerine'
  ];

  const leafName = commonNames[result.classIndex] || 'Unknown';
  const wikiLink = webLinks[result.classIndex] || '#';

  return (
    <div className="result-section">
      <div className="leaf-name">{leafName}</div>
      <a
        href={wikiLink}
        target="_blank"
        rel="noopener noreferrer"
        className="wikipedia-link"
      >
        Learn more on Wikipedia
      </a>
    </div>
  );
};

export default Result;