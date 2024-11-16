const inputImageButton = document.querySelector('#input-image-button');
const inputImageFile = document.querySelector('#input-image-file');
const inputImage = document.querySelector('#input-image');
const inputSubmit = document.querySelector('#input-submit');
const loading = document.querySelector('#loading');
const output = document.querySelector('#output');
const outputDetected = document.querySelector('#output-detected');
const outputRecognized = document.querySelector('#output-recognized');
const outputImage = document.querySelector('#output-image');
const outputPlates = document.querySelector('#output-plates');
const outputPlateTemplate = document.querySelector('#output-plate-template');

async function handleUpload() {
    try {
        output.hidden = true;
        inputImage.hidden = true;
        inputSubmit.hidden = true;
        const file = inputImageFile.files[0];
        if (!file)
            return;
        const reader = new FileReader();
        reader.readAsDataURL(file);
        inputImage.src = await new Promise((resolve, reject) => {
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
        });
        await new Promise((resolve, reject) => {
            inputImage.onload = resolve;
            inputImage.onerror = reject;
        });
        inputImage.hidden = false;
        inputSubmit.hidden = false;
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    } catch (error) {
        console.error(error);
        alert('Не удалось загрузить изображение');
    }
}

async function handleSubmit() {
    try {
        loading.hidden = false;
        output.hidden = true;
        inputSubmit.hidden = true;
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
        const file = inputImageFile.files[0];
        const data = new FormData();
        data.append('image', file);
        const response = await fetch('/api/predict', { method: 'POST', body: data });
        if (!response.ok)
            throw new Error(`HTTP Error ${response.status}`);
        const result = await response.json();
        handleResponse(result);
    } catch (error) {
        loading.hidden = true;
        inputSubmit.hidden = false;
        console.error(error);
        alert('Не удалось обработать запрос');
    }
}

async function handleResponse(result) {
    try {
        outputDetected.textContent = result.detected;
        outputRecognized.textContent = result.recognized;
        outputImage.src = result.image;
        outputPlates.replaceChildren();
        for (const plate of result.plates) {
            const outputPlate = outputPlateTemplate.content.cloneNode(true);
            const outputPlateNumber = outputPlate.querySelector('.output-plate-number');
            const outputPlateAccuracy = outputPlate.querySelector('.output-plate-accuracy');
            const outputPlateCoordinates = outputPlate.querySelector('.output-plate-coordinates');
            const outputPlateSizes = outputPlate.querySelector('.output-plate-sizes');
            outputPlateNumber.textContent = plate.number ?? '?';
            outputPlateAccuracy.textContent = `${(plate.accuracy * 100).toFixed(2)}%`;
            outputPlateCoordinates.textContent = `${plate.x}, ${plate.y}`;
            outputPlateSizes.textContent = `${plate.width} x ${plate.height}`;
            outputPlates.append(outputPlate);
        }
        await new Promise((resolve, reject) => {
            outputImage.onload = resolve;
            outputImage.onerror = reject;
        });
        output.hidden = false;
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    } catch (error) {
        console.error(error);
        alert('Не удалось вывести результат');
    } finally {
        loading.hidden = true;
        inputSubmit.hidden = false;
    }
}

inputImageButton.addEventListener('click', () => inputImageFile.click());
inputImageFile.addEventListener('change', handleUpload);
inputSubmit.addEventListener('click', handleSubmit);
