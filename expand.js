const axios = require('axios');

function extractLatLngFromUrl(url) {
    const patterns = [
        /[@/](-?\d+\.\d+),(\+?-?\d+\.\d+)[,?]/,
        /(-?\d+\.\d+),(-?\d+\.\d+)/
    ];

    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match) {
            return {
                lat: parseFloat(match[1]),
                lng: parseFloat(match[2])
            };
        }
    }

    return null;
}

module.exports = async (req, res) => {
    if (req.method === 'POST') {
        const { url } = req.body;
        
        if (!url) {
            return res.status(400).json({ error: 'No URL provided' });
        }

        try {
            const response = await axios.get(url, { maxRedirects: 5 });
            const finalUrl = response.request.res.responseUrl;
            const coordinates = extractLatLngFromUrl(finalUrl);

            res.status(200).json({ finalUrl, coordinates });
        } catch (error) {
            res.status(500).json({ error: 'Error expanding URL' });
        }
    } else {
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
};
