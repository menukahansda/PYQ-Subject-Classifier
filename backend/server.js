import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
dotenv.config();

import multer from 'multer';

const app = express();
const PORT = process.env.PORT || 8000;

const multerMiddleware = multer({ storage: multer.memoryStorage() });

app.use(cors());
app.use(express.json());

app.get('/', (req, res)=>{
    res.send('Just a get request!');
});

app.post('/process-pdfs', multerMiddleware.array('pdfs'), (req, res)=>{
    const pdfs = req.files;
    if (!pdfs || pdfs.length === 0) {
        return res.status(400).json({ error: 'No PDF files uploaded' });
    }
    console.log('Received PDF files:', pdfs.map(f => f.originalname));
    res.json({ message: 'PDF files received and processed successfully' });
});


app.listen(PORT,  ()=>{
    console.log(`Server is running on port ${PORT}`);
});