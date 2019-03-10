import { Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import { Validators, FormBuilder } from '@angular/forms';
import { CommentService } from 'src/app/api/comment.service';
import { Comment } from 'src/app/blog/models/comment';

@Component({
  selector: 'app-comment-create',
  templateUrl: './comment-create.component.html',
  styleUrls: ['./comment-create.component.css']
})
export class CommentCreateComponent implements OnInit {
  @Input() postId: number;
  @Input() parentComment: Comment;
  @Output() created = new EventEmitter<Comment>()

  commentForm = this.formBuilder.group({
    body: ['', Validators.required], 
    })
  
  constructor(
    private commentService: CommentService,
    private formBuilder: FormBuilder,
  ) { }

  ngOnInit() {
  }

  validateFormState() {
    const commentFormControls = this.commentForm.controls
    if (commentFormControls.body.valid === false) {
      alert('댓글 내용을 입력해주세요.')
      return false;
    } else {
      return true;
    }
  }

  onSubmit() {
    let postId = this.postId
    let form = this.commentForm.value
    let parentCommentId = this.parentComment? this.parentComment.id: undefined;

    if (!this.validateFormState()) {
      return;
    }

    this.commentService.createComment(form, postId, parentCommentId)
    .subscribe(comment => {
      this.created.emit(comment);
      this.commentForm.reset();
    })
  }
}

