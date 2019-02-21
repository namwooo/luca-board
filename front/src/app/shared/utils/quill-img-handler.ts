import { saveAs } from 'file-saver';


export function selectLocalImage() {
    const input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.click();
  
    // Listen upload local image and save to server
    input.onchange = () => {
      const file = input.files[0];
      console.log(file)
      if (file != null) {
        saveAs(file, 'image1.png')
        const range = this.getSelection();
        this.insertEmbed(range.index, 'image')
      }
      // file type is only image.
      if (/^image\//.test(file.type)) {
        // saveToServer(file);
        // saveToFileSystem(file);
      } else {
        console.warn('You could only upload images.');
      }
    };
  }
         
// function saveToServer(file: File) {
// console.log('call save to server')
// const fd = new FormData();
// fd.append('image', file);

// const xhr = new XMLHttpRequest();
// xhr.open('POST', 'http://localhost:5000/upload/image', true);
// xhr.onload = () => {
//     if (xhr.status === 200) {
//     // this is callback data: url
//     const url = JSON.parse(xhr.responseText).data;
//     // insertToEditor(url);
//     }
// };
// xhr.send(fd);
// }

// function saveToFileSystem(file: File) {
//     console.log('call save to filesystem')
//     saveAs(file, 'image.png')
//     insertToEditor('/Users/lucakim/Downloads');
// }

// function insertToEditor(url: string) {
// // push image url to rich editor.
//     const range = this.quill.getSelection();
//     this.quill.insertEmbed(range.index, 'image', url);
// }
