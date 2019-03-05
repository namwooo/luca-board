import { Component, OnInit, Input } from '@angular/core';
import { FormControl, Validators, FormBuilder } from '@angular/forms';
import { CommentService } from 'src/app/api/comment.service';
import { Post } from 'src/app/blog/models/post';

@Component({
  selector: 'app-comment-form',
  templateUrl: './comment-form.component.html',
  styleUrls: ['./comment-form.component.css']
})
export class CommentFormComponent implements OnInit {
  @Input() post: Post;
  @Input() comments: Comment[];
  @Input() commentId: Number;

  commentForm = this.formBuilder.group({
    body: ['', Validators.required], 
    })
  
  constructor(
    private commentService: CommentService,
    private formBuilder: FormBuilder,
  ) { }

  ngOnInit() {
  }

  onSubmit(): void {
    let body = this.commentForm.value
    console.log(body)
    this.commentService.createComment(this.commentForm.value, this.post.id, this.commentId)
    .subscribe(comment => console.log(comment))
  }

    // todo: remove this after dev
    get diagnostic() { return JSON.stringify(this.commentForm.value); }
}
