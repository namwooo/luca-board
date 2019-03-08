import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Post } from '../../models/post';
import { Router } from '@angular/router';

@Component({
  selector: 'app-post-nav',
  templateUrl: './post-nav.component.html',
  styleUrls: ['./post-nav.component.css']
})
export class PostNavComponent implements OnInit {
  @Input() post: Post;

  constructor(
    private router: Router,
  ) { }

  ngOnInit() {
  }

  onClickPrevious(): void {
    let prevPostId = this.post.prevPost.id
    this.router.navigate([`/posts/${prevPostId}`])

  }

  onClickNext(): void {
    let nextPostId = this.post.nextPost.id
    this.router.navigate([`/posts/${nextPostId}`])
  }

}
