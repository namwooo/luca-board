import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { CommentService } from 'src/app/services/comment.service';

@Component({
  selector: 'app-comment-form',
  templateUrl: './comment-form.component.html',
  styleUrls: ['./comment-form.component.css']
})
export class CommentFormComponent implements OnInit {
  body = new FormControl('');

  constructor(
    private commentService: CommentService
  ) { }

  ngOnInit() {
  }

  // onSubmit(): void {
  //   this.commentService.createComment(this.body)
  //   .subscribe(comment => console.log(comment))
  // }

    // todo: remove this after dev
    get diagnostic() { return JSON.stringify(this.body.value); }

}
