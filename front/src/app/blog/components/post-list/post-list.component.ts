import { Component, OnInit, OnChanges, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Post } from 'src/app/blog/models/post';
import { PostService } from 'src/app/api/post.service';
import { BoardService } from 'src/app/api/board.service';
import { Board } from 'src/app/blog/models/board';

@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent implements OnInit {
  posts: Post[];
  board: Board;
  
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

  getPostsInBoard(id: number): void {
    this.postService.getPostsInBoard(id)
    .subscribe(posts => {
      this.posts = posts['items']
    });
  }

  getBoard(id: number): void {
    this.boardService.getBoard(id)
    .subscribe(board => {
      this.board = board
    })
  }
}
