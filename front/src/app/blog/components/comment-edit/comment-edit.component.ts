import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { Comment } from 'src/app/blog/models/comment';
import { CommentService } from 'src/app/api/comment.service';

@Component({
  selector: 'app-comment-edit',
  templateUrl: './comment-edit.component.html',
  styleUrls: ['./comment-edit.component.css']
})
export class CommentEditComponent implements OnInit {
  @Input() targetComment: Comment;
  @Output() edited = new EventEmitter<string>();
  commentForm: FormGroup;
  
  constructor(
    private formBuilder: FormBuilder,
    private commentService: CommentService,
    ) { }

  ngOnInit() {
    this.commentForm = this.formBuilder.group({
      body: [this.targetComment.body, Validators.required], 
      })
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
    let id = this.targetComment.id
    let form = this.commentForm.value

    if(!this.validateFormState()){
      return;
    }

    this.commentService.updateComment(id, form)
    .subscribe(resp => this.edited.emit(form.body))
  }
}
