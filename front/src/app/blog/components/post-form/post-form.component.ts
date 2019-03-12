import { Component, OnInit } from '@angular/core';
import { Board } from 'src/app/blog/models/board';
import { BoardService } from 'src/app/api/board.service';
import { PostService } from 'src/app/api/post.service';
import { FormBuilder, Validators} from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { Post } from '../../models/post';

@Component({
  selector: 'app-post-form',
  templateUrl: './post-form.component.html',
  styleUrls: ['./post-form.component.css']
})
export class PostFormComponent implements OnInit {
  boards: Board[];
  id: number;
  isEdit: Boolean
  post: Post;
  // set PostCreateForm
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
    private route: ActivatedRoute,
    ) { }

  ngOnInit() {
    this.route.params.subscribe(params => this.id = params.id);
    this.route.data.subscribe(data => this.isEdit = data.isEdit);
    this.getBoards();
    this.setPostEditForm();
  }
  
  setPostEditForm(): void {
    if (this.id) {
      this.postService.getPost(this.id)
      .subscribe(post => {
        this.post = post;
        this.postForm = this.formBuilder.group({
          idBoard: [this.post.board.id, Validators.required], 
          title: [`${this.post.title}`, Validators.required],
          body: [`${this.post.body}`, Validators.required],
          isPublished: [this.post.isPublished, Validators.required]
        })
      }) 
    } 
  }

  onSubmit(): void {
    /* Validate state of form control */
    this.validateFormState();

    /* Assign body and param */
    let idBoard = this.postForm.value.idBoard
    let body = this.postForm.value
    delete body.idBoard

    if (this.postForm.value.body.includes('img')) {
      body['has_image'] = true
    } else {
      body['has_image'] = false
    }

    if (this.isEdit) {
      this.postService.updatePost(body, this.post.id)
      .subscribe(post => console.log(post))
    } else {
      this.postService.createPost(body, idBoard)
      .subscribe(post => console.log(post));
    }
  }

  validateFormState() {
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
  }

  getBoards(): void {
    this.boardService.getBoards()
    .subscribe(boards => this.boards = boards);
  }

  getPost(id: number): any {
    this.postService.getPost(id)
    .subscribe(post => this.post = post);
  }


  // todo: remove this after dev
  get diagnostic() { return JSON.stringify(this.postForm.value); }
}