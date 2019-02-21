import { Component, OnInit, Input } from '@angular/core';
import { selectLocalImage } from 'src/app/shared/utils/quill-img-handler';
import { PostForm } from 'src/app/models/post-form';
import * as Quill from 'quill';

@Component({
  selector: 'app-quill-editor',
  templateUrl: './quill-editor.component.html',
  styleUrls: ['./quill-editor.component.css']
})
export class QuillEditorComponent implements OnInit {
  @Input() postForm: PostForm;

  constructor() { }

  ngOnInit() {
  }

  getEditorInstance(editorInstance: any) {
    let toolbar = editorInstance.getModule('toolbar');
    toolbar.addHandler('image', selectLocalImage.bind(editorInstance))
    console.log(toolbar.handlers)
  }
}
