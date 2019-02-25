import { Component, OnInit } from '@angular/core';
import { Board } from 'src/app/models/board';
import { BoardService } from 'src/app/services/board.service';
import { PostService } from 'src/app/services/post.service';
import { Router } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { selectLocalImage } from 'src/app/shared/utils/quill-img-handler';

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
    private router: Router,
    private formBuilder: FormBuilder,
    ) { }

  ngOnInit() {
    this.getBoards();
  }

  onSubmit(): void {
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

    this.postService.createPost(this.postForm.value)
    .subscribe(post => this.router.navigate([`/boards/${post['idBoard']}`]));
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