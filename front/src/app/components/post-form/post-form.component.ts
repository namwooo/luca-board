import { Component, OnInit } from '@angular/core';
import { Board } from 'src/app/models/board';
import { BoardService } from 'src/app/services/board.service';
import { Post } from 'src/app/models/post';
import { PostService } from 'src/app/services/post.service';
import { Router } from '@angular/router';
import { FormGroup, FormControl } from '@angular/forms';
import { selectLocalImage } from 'src/app/shared/utils/quill-img-handler';

@Component({
  selector: 'app-post-form',
  templateUrl: './post-form.component.html',
  styleUrls: ['./post-form.component.css']
})
export class PostFormComponent implements OnInit {
  boards: Board[];
  postForm = new FormGroup({
    idBoard: new FormControl,
    title: new FormControl(''),
    body: new FormControl(''),
    isPublished: new FormControl(true),
  })

  constructor(
    private boardService: BoardService,
    private postService: PostService,
    private router: Router
    ) { }

  ngOnInit() {
    this.getBoards();
  }

  onSubmit(): void {
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