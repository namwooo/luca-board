import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-like-toggle',
  templateUrl: './like-toggle.component.html',
  styleUrls: ['./like-toggle.component.css']
})
export class LikeToggleComponent implements OnInit {
  @Input() isUserLike: boolean;
  @Output() liked = new EventEmitter<boolean>();
  
  constructor() { }

  ngOnInit() {
  }

  likeToggle(like: boolean) {
    this.liked.emit(like)
    like ? this.isUserLike = true: this.isUserLike = false
  }
}
