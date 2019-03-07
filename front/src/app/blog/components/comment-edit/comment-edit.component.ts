import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-comment-edit',
  template: `<a (click)="onClickEdit(targetComment)">수정</a>`,
  styleUrls: ['./comment-edit.component.css']
})
export class CommentEditComponent implements OnInit {
  @Input() targetComment: Comment;
  
  constructor() { }

  ngOnInit() {
  }

  onClickEdit() {
    
  }

}
