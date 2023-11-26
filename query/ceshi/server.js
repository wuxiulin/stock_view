const express = require('express');
const fetch = require('node-fetch');
const app = express();
const PORT = 3000;

app.get('/', async (req, res) => {
    try {
        // 使用node-fetch库获取目标网页的内容
        const response = await fetch('http://data.10jqka.com.cn/hsgt/index');
        const html = await response.text();
        
        // 将获取的HTML发送到前端
        res.send(html);
    } catch (error) {
        console.error('Error fetching content:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
