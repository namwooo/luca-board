import { Component, OnInit } from '@angular/core';
import { Post } from '../../models/post';
import { PostService } from 'src/app/api/post.service';

@Component({
  selector: 'app-post-rank',
  templateUrl: './post-rank.component.html',
  styleUrls: ['./post-rank.component.css']
})
export class PostRankComponent implements OnInit {
  posts: Post[];
  
  constructor(
    private postService: PostService,
  ) { }

  ngOnInit() {
    this.getPostsRank();
  }

  getPostsRank() {
    this.postService.getPostsRank()
    .subscribe(posts => this.posts = posts);
  }

}
