// dashboard - product-new.html

FilePond.registerPlugin(FilePondPluginImagePreview);
FilePond.registerPlugin(FilePondPluginFileMetadata);
FilePond.registerPlugin(FilePondPluginFileRename);

// Get a reference to the file input element
const inputElements = document.querySelector(`#mainfileimages`);
const inputElement = document.querySelector(`#mainfile`);

// Create a FilePond instance
const pondimages = FilePond.create(inputElements,{
        server: './upload-p-images',
        credits: false,
        labelIdle: "Drop or Browse images",
        fileMetadataObject: {
            p_id: product_data['id'],
        },
        fileRenameFunction: (file) => {
            let _st = fname(19);
            images.push(_st+`${file.extension}`)
            return _st+`${file.extension}`;
        },
});

const pond = FilePond.create(inputElement, {
        server: './upload-p-main',
        labelIdle: "Main image",
        credits: false,
        fileMetadataObject: {
            p_id: product_data['id'],
        },
        fileRenameFunction: (file) => {
            let _st = fname(19);
            product_data['mainimage'] = _st+`${file.extension}`;
            return _st+`${file.extension}`;
        },
});

pond.on('removefile', (error, file) => {
product_data['mainimage'] = "";
})

pondimages.on('removefile', (error, file) => {
images = images.filter(v => v !== file.filename);
})