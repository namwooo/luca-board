import { Component, OnInit, Input } from '@angular/core';
import { CommentService } from 'src/app/api/comment.service';
import { Comment } from 'src/app/blog/models/comment';

@Component({
  selector: 'app-comment-list',
  templateUrl: './comment-list.component.html',
  styleUrls: ['./comment-list.component.css']
})
export class CommentListComponent implements OnInit {
  @Input() postId: number;
  comments: Comment[];
  targetCommentId: number;
  isCommentFormInserted = false;

  constructor(
    private commentService: CommentService,
  ) { }

  ngOnInit() {
    this.getCommentsInPost(this.postId);
  }

  getCommentsInPost(postId: number) {
    this.commentService.getCommentsInPost(postId)
    .subscribe(comments => this.comments = comments)
  }
  
  insertCommentForm(event: any) {
    if (this.targetCommentId != event.target.id) {
      this.isCommentFormInserted= true;
      this.targetCommentId = event.target.id;
    } else if (this.isCommentFormInserted) {
      this.isCommentFormInserted = false;
    } else {
      this.targetCommentId = event.target.id;
      this.isCommentFormInserted= true;
    }
  }
}
