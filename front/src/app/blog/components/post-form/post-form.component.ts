import { Component, OnInit } from '@angular/core';
import { Board } from 'src/app/blog/models/board';
import { BoardService } from 'src/app/api/board.service';
import { PostService } from 'src/app/api/post.service';
import { FormBuilder, Validators } from '@angular/forms';
import { selectLocalImage } from 'src/app/utils/quill-img-handler';

@Component({
  selector: 'app-post-form',
  templateUrl: './post-form.component.html',
  styleUrls: ['./post-form.component.css']
})
export class PostFormComponent implements OnInit {
  boards: Board[];
  postForm = this.formBuilder.group({
    idBoard: ['', Validators.required], 
    title: ['', Validators.required],
    body: ['', Validators.required],
    isPublished: [true, Validators.required]
    })

  constructor(
    private boardService: BoardService,
    private postService: PostService,
    private formBuilder: FormBuilder,
    ) { }

  ngOnInit() {
    this.getBoards();
  }

  onSubmit(): void {
    /* Validate state of form control */
    const postFormControls = this.postForm.controls
    if (postFormControls.idBoard.valid === false) {
      alert('게시판을 선택해주세요.')
      return;
    }
    if (postFormControls.title.valid === false) {
      alert('게시글 제목을 입력해주세요.')
      return;
    }
    if (postFormControls.body.valid === false) {
      alert('게시글 내용을 입력해주세요.')
      return;
    }
    if (postFormControls.isPublished.valid === false) {
      alert('공개 여부를 선택해주세요.')
      return;
    }
    
    /* Assign body and param */
    let idBoard = this.postForm.value.idBoard
    let body = this.postForm.value
    delete body.idBoard
    
    /* Call post service */
    this.postService.createPost(body, idBoard)
    .subscribe(post => console.log(post));
  }

  getEditorInstance(editorInstance: any) {
    let toolbar = editorInstance.getModule('toolbar');
    toolbar.addHandler('image', selectLocalImage.bind(editorInstance))
  }

  getBoards(): void {
    this.boardService.getBoards()
    .subscribe(boards => this.boards = boards);
  }


  // todo: remove this after dev
  get diagnostic() { return JSON.stringify(this.postForm.value); }
}