import { Component, OnInit } from '@angular/core';
import { CommentService } from 'src/app/services/comment.service';
import { Comment } from 'src/app/models/comment';

@Component({
  selector: 'app-comment-list',
  templateUrl: './comment-list.component.html',
  styleUrls: ['./comment-list.component.css']
})
export class CommentListComponent implements OnInit {
  comments: Comment[];
  addComment = false;
  idComment: number;

  constructor(
    private commentService: CommentService,
  ) { }

  ngOnInit() {
    this.getCommentsInPost(1);
  }

  getCommentsInPost(id: number) {
    this.commentService.getCommentsInPost(id)
    .subscribe(comments => this.comments = comments)
  }
  
  addCommentForm(event: any) {
    this.idComment = event.target.id;
    if (this.addComment) {
      this.addComment = false;
    } else {
      this.addComment= true;
    }
  }
}
