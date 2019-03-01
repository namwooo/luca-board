import { Component, OnInit, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
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
  @Input() idComment: number;
  commentForm = new FormControl('');

  constructor(
    private commentService: CommentService
  ) { }

  ngOnInit() {
  }

  onSubmit(): void {
    this.commentService.createComment(this.commentForm.value, this.post.id, this.idComment)
    .subscribe(comment => console.log(comment))
  }

    // todo: remove this after dev
    get diagnostic() { return JSON.stringify(this.commentForm.value); }
}
