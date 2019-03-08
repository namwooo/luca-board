import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Post, PagedPost } from 'src/app/blog/models/post';
import { PostService } from 'src/app/api/post.service';
import { BoardService } from 'src/app/api/board.service';

@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent implements OnInit {
  posts: Post[];
  boardTitle: string;
  
  constructor(
    private postService: PostService,
    private boardService: BoardService,
    private route: ActivatedRoute,
    ) { }
  
  ngOnInit() {
    this.route.params.subscribe(
      params => {
        let id = +params['id']
        this.getPostsInBoard(id);
        this.getBoard(id);
      }
    )
  }
  
  getBoard(boardId: number): void {
    this.boardService.getBoard(boardId)
    .subscribe(board => {
      this.boardTitle = board.title;
    })
  }

  getPostsInBoard(boardId: number): void {
    this.postService.getPostsInBoard(boardId)
    .subscribe(posts => {
      this.posts = posts['items'];
    });
  }
}
