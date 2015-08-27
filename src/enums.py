# -*- coding: utf-8 -*-

import os

# Smaller list of cities for testing purposes
SOME_CITY_NAMES = {
	'CITIES': [
		'Calgary',
		'Berlin',
		'Tokyo',
		'London'
	]
}

# List of all cities to calculate the sunset for
ALL_CITY_NAMES = {
	'AFRICA': [
		'Accra',
		'Dakar',
		'Pretoria',
		'Tripoli',
		'Abuja',
		'Kampala',
		'Bamako',
		'Rabat',
		'Antananarivo',
		'Ouagadougou',
		'Conakry',
		'Tunis',
		'Freetown',
		'Monrovia',
	#Central Africa
		#Burkina Faso
		'Ouagadougou',
		'Bobo Dioulasso',
		'Banfora',
		'Koudougou',
		#Chad
		'N\'Djamena',
		'Moundou',
		'Sarh',
		'Abeche',
		'Kelo',
		#Democratic republic of Congo
		'Kinshasa',
		'Lubumbashi',
		'Mbuji-Mayi',
		'Kananga',
		'Kisangani',
		'Tshikapa',
		'Kolwezi',
		'Likasi',
		'Kikwit',
		#Republic of Congo
		'Brazzaville',
		'Pointe-Noire',
		'Dolisie',
		'Nkayi',

		'Malabo',
		'Libreville',
	#East Africa
		#Burundi
		'Bujumbura',
		'Gitega',
		#Cameroon
		'Douala',
		'Yaounde',
		'Bamenda',
		'Bafoussam',
		'Garoua',
		'Maroua',
		'Ngaoundere',
		'Kumba',
		'Buea',
		'Nkongsamba',
		#Djibouti
		'Djibouti City',
		'Ali Sabieh',
		#Equatoril Guinea
		'Malabo',

		#Ethiopia
		'Addis Ababa',
		'Mek\'ele',
		'Dire Dawa',
		'Adama',
		'Gondar',
		
		'Hahaya',
		
		'Mombasa',
		'Nairobi',
		'Kigali',
		'Entebbe',
	#Horn of Africa
		'Djibouti City',
		'Asmara',
		'Mogadishu',
		#Bennin
		'Cotonou',
		'Porto Novo',
		'Parakou',
		'Djougou',
		'Bohicon',
		'Kandi',
		'Abomey',
		'Natitingou',
		'Lokossa',
		'Ouidah',
		#Eritrea
		'Asmara',
		'Keren',
		'Teseney',

	#North Africa
		#Algeria
		'Algiers',
		'Oran',
		'Constantine',
		'Annaba',
		'Blida',
		'Batna',
		'Djelfa',
		'Setif',
		'Sidi Bel Abbes',
		'Biskra',

		'Cairo',
		'Benghazi',
		'Sebha',
		'Casablanca',
		'Marrakech',
		'Khartoum',
		'Djerba',
		'Monastir',
		'Carthage',
		'Dakhla',
	#Southern Africa
		#Angoloa
		'Luanda',
		'Cabinda',
		'Huambo',
		'Lubango ',
		'Kuito',
		'Malanje',
		'Lobito',
		'Benguela',
		'Uige',
		#Botswana
		'Gaborone',
		'Francistown',
		'Molepolole',
		'Lubango',
		'Maun',
		'Maseru',
		'Mahajanga',
		'Toamasina',
		'Toliara',
		'Maputo',
		'Windhoek',
		'Cape Town',
		'Johannesburg',
		'Manzini',
		'Lusaka',
		'Harare',
	],
	'AMERICAS': [
		'Buenos Aires',
		'Lima',
		'Santiago',
		'Brasilia',
		'Seattle',
		'Santo Domingo',
		'Caracas',
		'San Juan',
	# Canada
		'Calgary',
		'Charlottetown',
		'Edmonton',
		'Fredericton',
		'Halifax',
		'Hamilton',
		'Iqaluit',
		'Kelowna',
		'Moncton',
		'Montreal',
		'Ottawa',
		'Quebec City',
		'Regina',
		'Saskatoon',
		'St. John\'s',
		'Toronto',
		'Vancouver',
		'Victoria',
		'Whitehorse',
		'Winnipeg',
		'Yellowknife',
	# United States
		'Albany',
		'Albuquerque',
		'Anchorage',
		'Atlanta',
		'Austin',
		'Baltimore',
		'Boston',
		'Chicago',
		'Cincinnati',
		'Cleveland',
		'Dallas',
		'Denver',
		'Detroit',
		'Fargo',
		'Honolulu',
		'Houston',
		'Indianapolis',
		'Jacksonville',
		'Kansas City',
		'Las Vegas',
		'Los Angeles',
		'Louisville',
		'Memphis',
		'Miami',
		'Milwaukee',
		'Minneapolis',
		'Nashville',
		'New Orleans',
		'New York',
		'New Jersey',
		'Oakland',
		'Palm Springs',
		'Philadelphia',
		'Phoenix',
		'Pittsburgh',
		'Portland',
		'Raleigh',
		'Reno',
		'Sacramento',
		'Salt Lake City',
		'San Diego',
		'San Francisco',
		'San Jose',
		'Seattle',
		'Spokane',
		'Syracuse',
		'Tampa',
		'Tulsa',
		'Washington DC',
		'Yuma',
	#Mexico
		'Acapulco',
		'Cabo San Lucas',
		'Chihuahua',
		'Guadalajara',
		'Mexico City',
		'Monterrey',
		'Tijuana',
		'Villahermosa',
	#Caribbean
		'Aguadilla',
		'Belize City',
		'Nassau',
		'Georgetown',
		'Havana',
		'Flores',
		'Guatemala City',
		'Panama City',
		'Santa Clara',
		'San Juan',
		'Santiago de los Caballeros',
		'San Jose de Costa Rica',
		'San Salvador',
		'Grenada',
		'Port-au-Prince',
		'Kingston',
		'Montego Bay',
		'Tobago',
		'Tegucigalpa',
	#Central America
	#South America
		'Antofagasta',
		'Buenos Aires',
		'Mendoza',
		'Brasilia',
		'Curitiba',
		'Rio de Janeiro',
		'Santiago',
		'Cali',
		'Quito',
		'Cusco',
		'Lima',
		'Montevideo',
		'Caracas',
		'Maracaibo'
	],
	'ASIA': [
	#Central Asia
		'Aktobe',
		'Andijan',
		'Almaty',
		'Astana',
		'Uralsk',
		'Bishkek',
		'Bukhara',
		'Chust',
		'Dushanbe',
		'Herat',
		'Isfara',
		'Jilikul',
		'Karaganda',
		'Kashgar',
		'Kunduz',
		'Mazar-i-Sharif',
		'Merv',
		'Muborak',
		'Samarkand',
		'Shymkent',
		'Urumqi',
		'Vose',
		'Yovon',
		'Khujand',
		'Ashgabat',
		'Namangan',
		'Tashkent',
	#East Asia
		#NorthKorea
		'Pyongyang',
		'Hamhung',
		'Chongjin',
		'Nampo',
		'Wonsan',
		'Sinuiju',
		'Tanchon',
		'Kaechon',
		'Kaesong',
		'Sariwon',
		'Hong Kong',
		#Japan
		'Yokohama',
		'Kobe',
		'Kyoto',
		'Fukuoka',
		'Kawasaki',
		'Saitama',
		'Sendai',
		'Kitakyushu',
		'Chiba',
		'Sakai',
		'Niigata',
		'Hamamatsu',
		'Kumamoto',
		'Sagamihara',
		'Shizuoka',
		'Hiroshima',
		'Nagasaki',
		'Osaka',
		'Sapporo',
		'Tokyo',
		'Nagoya',
		'Macau',
		#Mongolia
		'Ulan Bator',
		'Erdenet',
		'Darkhan',
		'Choibalsan',
		'Moron',
		#China
		'Beijing',
		'Shanghai',
		'Guangzhou',
		'Shenzhen',
		'Chongqing',
		'Hangzhou',
		'Wuhan',
		'Harbin',
		'Kunming',
		'Dongguan',
		'Chengdu',
		'Nanjing',
		'Shenyang',
		'Suzhou',
		'Jinan',
		'Xi\'an',
		'Wuxi',
		'Hefei',
		'Changchun',
		'Changzhou',
		'Dalian',
		'Taiyuan',
		'Zhengzhou',
		'Changsha',
		'Ningbo',
		'Qingdao',
		'Zibo',
		'Fuzhou',
		'Nanning',	
		#SouthKorea
		'Busan',
		'Seoul',
		'Incheon',
		'Daegu',
		'Daejeon',
		'Gwangju',
		'Ulsan',
		'Suwon',
		'Changwon',
		'Seongnam',
		'Goyang',
		'Yongin',
		'Bucheon',
		'Ansan',
		'Cheongju',
		'Jeonju',
		'Anyang',
		'Cheonan',
		'Namyangju',
		'Pohang',
		#Taiwan
		'Taipei',
		'Kaohsiung',
		'Taichung',
		'Tainan',
		'Hsinchu',
		'Taoyuan',
		'Keelung',
		'Zhongli',
		'Chiayi',
		'Changhua',
		'Pingtung',
		'Pingzhen',
		'Bade',
		'Yangmei',
		'Tianjin',
		'Shenyang',

	#South Asia
		'Chittagong',
		'Dhaka',
		'Sylhet',
		'Bangalore',
		'Delhi',
		'Mumbai',
		'Kathmandu',
		'Islamabad',
		'Karachi',
		'Colombo',
		'Hambantota',
		'Ahmedabad',
		'Kolkata',
		'Chennai',
		'Hyderabad',
		'Ahmedabad',

	#South East Asia
		'Phnom Penh',
		'Makassar',
		'Palembang',
		'Jakarta',
		'Balikpapan',
		'Kendari',
		'Kuala Lumpur',
		'Penang',
		'Mandalay',
		'Langkawi',
		'Manila',
		'Kalibo',
		'Singapore',
		'Bangkok',
		'Chiang Mai',
		'Phuket',
		'Ko Samui',
		'Hai Phong',
	#South West Asia
		'Kabul',
		'Kandahar',
		'Shiraz',
		'Birjand',
		'Tehran',
		'Isfahan',
		'Baghdad',
		'Basra',
		'Tel Aviv',
		'Aqaba',
		'Kuwait City',
		'Beirut',
		'Muscat',
		'Doha',
		'Mecca',
		'Dammam',
		'Medina',
		'Jeddah',
		'Riyadh',
		'Damascus',
		'Latakia',
		'Abu Dhabi',
		'Dubai'
	],
	'EUROPE': [
		'Tirana',
		'Yerevan',
		'Gyumri',
		'Baku',
		'Ganja',
		'Nakhchivan',
		'Graz',
		'Klagenfurt',
		'Innsbruck',
		'Linz',
		'Salzburg',
		'Vienna',
		'Hrodna',
		'Gomel',
		'Minsk',
		'Antwerp',
		'Brussels',
		'Banja Luka',
		'Sarajevo',
		'Tuzla',
		'Mostar',
		'Burgas',
		'Plovdiv',
		'Sofia',
		'Varna',
		#Crotia
		'Dubrovnik',
		'Osijek',
		'Pula',
		'Rijeka',
		'Split',
		'Zadar',
		'Zagreb',
		#Cyprus
		'Larnaca',
		'Paphos',
		'Ercan',
		#Czech
		'Brno',
		'Jihlava',
		'Karlovy Vary',
		'Liberec',
		'Olomouc',
		'Ostrava',
		'Opava',
		'Plzen',
		'Prague',
		'Pardubice',
		#Denmark
		'Aalborg',
		'Aarhus',
		'Odense',
		'Frederiksberg',
		'Esbjerg',
		'Gentofte',
		'Gladsaxe',
		'Randers',
		'Kolding',
		'Billund',
		'Copenhagen',
		#Estonia
		'Tallinn',
		'Tartu',
		'Narva',
		'Kohtla-Jarve',
		'Viljandi',
		'Maardu',
		'Kuressaare',
		#Finland
		'Helsinki',
		'Espoo',
		'Tampere',
		'Vantaa',
		'Oulu',
		'Lahti',
		'Kouvola',
		'Pori',
		'Joensuu'
		'Kuopio',
		'Kuusamo',
		'Lappeenranta',
		'Oulu',
		'Rovaniemi',
		'Tampere Pirkkala',
		'Turku',
		'Vaasa',
		#France
		'Ajaccio',
		'Bastia',
		'Beauvais',
		'Bergerac',
		'Biarritz',
		'Bordeaux',
		'Brest',
		'Carcassonne',
		'Champagne sur Oise',
		'Dinard',
		'Figari Sud Corse',
		'Grenoble Isrre',
		'Lille Lesquin',
		'Limoges',
		'Lyon',
		'Marseille',
		'Mulhouse',
		'Nantes',
		'Nice',
		'Nimes',
		'Paris',
		'Perpignan',
		'Poitiers',
		'Rodez',
		'Strasbourg',
		'Toulon',
		'Toulouse',
		#Georgia
		'Batumi',
		'Tbilisi',
		'Kutaisi',
		'Rustavi',
		'Zugdidi',
		'Gori',
		'Poti',
		'Samtredia',
		'Khashuri',
		'Senaki',
		#Germany
		'Baden',
		'Berlin',
		'Bremen',
		'Cologne',
		'Dortmund',
		'Dresden',
		'Essen',
		'Frankfurt',
		'Friedrichshafen',
		'Hamburg',
		'Hanover',
		'Leipzig',
		'Memmingen',
		'Munich',
		'Nuremberg',
		'Stuttgart',
		'Weeze',
		'Hamm',
		#Greece
		'Athens',
		'Chania',
		'Chios Island',
		'Corfu',
		'Heraklion',
		'Kalamata',
		'Karpathos Island',
		'Kavala',
		'Kefalonia Island',
		'Kos Island',
		'Mykonos Island',
		'Mytilene',
		'Preveza',
		'Rhodes',
		'Samos',
		'Santorini',
		'Skiathos Island',
		'Skyros Island',
		'Macedonia',
		'Volos',
		'Zakynthos',
		#Hungary
		'Budapest',
		'Debrecen',
		'Miskolc',
		'Szeged',
		'Gyor',
		#Iceland
		'Akureyri',
		'Reykjavik',
		'Kopavogur',
		'Akureyri',
		'Akranes',
		'Selfoss',
		#Ireland
		'Cork',
		'Dublin',
		'Kerry',
		'Knock',
		'Shannon',
		'Isle of Man',
		'Limerick',
		'Galway',
		'Waterford',
		'Drogheda',
		'Kilkenny',
		#Italy
		'Alghero',
		'Ancona',
		'Palese',
		'Bergamo',
		'Bologna',
		'Brescia',
		'Brindisi',
		'Cagliari',
		'Elmas',
		'Catania',
		'Cuneo Levaldigi',
		'Florence',
		'Genoa',
		'Lamezia Terme',
		'Milan',
		'Naples',
		'Olbia',
		'Palermo',
		'Parma',
		'Perugia',
		'Pescara',
		'Pisa',
		'Rimini',
		'Rome',
		'Trapani',
		'Trieste',
		'Turin',
		'Venice',
		'Verona',
		#Kosovo
		'Pristina',
		#Latvia
		'Riga',
		'Ventspils',
		'Daugavpils',
		#lithuania
		'Kaunas',
		'Palanga',
		'Siauliai',
		'Vilnius',
		#Luxembourg
		'Luxembourg',
		#Macedonia
		'Skopje',
		#Malta
		'Luqa',
		#Moldovia
		'Chisinau',
		#Montenegro
		'Podgorica',
		'Tivat',
		#Netherlands
		'Amsterdam',
		'Eindhoven',
		'Groningen',
		'Rotterdam',
		#Norway
		'Alesund',
		'Bergen',
		'Haugesund',
		'Oslo',
		'Stavanger',
		'Trondheim',
		'Kristiansand',
		'Fredrikstad',
		'Skien',
		#Poland
		'Bydgoszcz',
		'Katowice',
		'Krakow',
		'Warsaw',
		'Wroclaw',
		'Lodz',
		'Poznan',
		'Gdansk',
		'Szczecin',
		'Bydgoszcz',
		'Lublin',
		#Portugal
		'Funchal',
		'Porto Santo',
		'Lisbon',
		'Porto',
		'Ponta Delgada',
		'Terceira',
		#Romania
		'Bucharest',
		'Cluj-Napoca',
		'Constanta',
		'Iasi',
		'Sibiu',
		'Timisoara',
		#Russia
		'Arkhangelsk',
		'Chita',
		'Irkutsk',
		'Kazan',
		'Khabarovsk Krai',
		'Kaliningrad',
		'Krasnodar',
		'Moscow',
		'Novosibirsk',
		'Rostov on Don',
		'Saint Petersburg',
		'Samara',
		'Sochi',
		'Ufa',
		'Vladivostok',
		'Yakutsk',
		'Yekaterinburg',
		#Serbia
		'Belgrade',
		#Slovakia
		'Bratislava',
		'Kosice',
		'Zilina',
		#Slovenia
		'Ljubljana',
		#Spain
		'Alicante',
		'Asturias',
		'Barcelona',
		'Ciudad Real',
		'Fuerteventura',
		'Girona Costa Brava',
		'Gran Canaria',
		'Granada',
		'Huesca Pirineos',
		'Ibiza',
		'Santa Cruz de la Palma',
		'Lanzarote',
		'Lleida',
		'Madrid',
		'Minorca',
		'Murcia San Javier',
		'Palma de Mallorca',
		'Reus',
		'Santander',
		'Seville',
		'Tenerife',
		'Valencia',
		'Valladolid',
		'Zaragoza',
		#Sweden
		'Gothenburg',
		'Stockholm',
		'Visby',
		#Switzerland
		'Basel',
		'Bern',
		'Geneva',
		'Zurich',
		#Turkey
		'Adana',
		'Ankara',
		'Antalya',
		'Bodrum',
		'Bursa',
		'Dalaman',
		'Gaziantep',
		'Istanbul',
		'Izmir',
		'Kayseri',
		'Konya',
		'Malatya',
		'Nevsehir',
		'Samsun',
		'Trabzon',
		'Zonguldak',
		#Ukraine
		'Kiev',
		'Chernivtsi',
		'Donetsk',
		'Dnipropetrovsk',
		'Kharkiv',
		'Kryvyi Rih',
		'Kyiv Zhuliany',
		'Luhansk',
		'Odessa',
		'Mykolaiv',
		'Simferopol',
		'Zaporizhia',
		#United Kingdom
		'Aberdeen',
		'Belfast',
		'Birmingham',
		'Bournemouth',
		'Bristol',
		'Cardiff',
		'Derry',
		'Durham',
		'Edinburgh',
		'East Midlands',
		'Exeter',
		'Glasgow',
		'Inverness',
		'Leeds',
		'Liverpool',
		'London',
		'Manchester',
		'Newcastle',
		'Cornwall',
		'Norwich',
		'Sheffield',
		'Southampton'
	],
	'Oceania':[
		#Australia
		'Adelaide',
		'Brisbane',
		'Cairns',
		'Darwin',
		'Gold Coast',
		'Hobart',
		'Melbourne',
		'Perth',
		'Sydney',
		#New Zealand
		'Auckland',
		'Christchurch',
		'Dunedin',
		'Hamilton',
		'Queenstown',
		'Rotorua',
		'Wellington',
		#Islands
		'Christmas Island',
		'Keeling',
		'Rarotonga',
		'Nadi',
		'Suva',
		'Papeete',
		'Kiritimati',
		'Tarawa',
		'Kwajalein',
		'Majuro',
		'Chuuk',
		'Kosrae',
		'Pohnpei',
		'Yap',
		'Yaren',
		'Noumea',
		'Norfolk',
		'Saipan Island',
		'Rota Island',
		'Tinian Island',
		'Alofi',
		'Korror',
		'Port Moresby',
		'Apia',
		'Honiara',
		'Nuku\'alofa',
		'Funafuti',
		'Port Vila',
		'Futuna',
		'Wallis'
	]
}
