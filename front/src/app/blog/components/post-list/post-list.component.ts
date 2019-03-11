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
  perPage: number;
  page: number;
  total: number;
  boardTitle: string;
  boardId: number;
  
  constructor(
    private postService: PostService,
    private boardService: BoardService,
    private route: ActivatedRoute,
    ) { }
  
  ngOnInit() {
    this.route.params.subscribe(
      params => {
        let id = +params['id']
        console.log(id);
        this.boardId = id;
        this.getPostsInBoard();
        this.getBoard();
      }
    )
  }
  
  getBoard() {
    this.boardService.getBoard(this.boardId)
    .subscribe(board => {
      this.boardTitle = board.title;
    })
  }

  getPostsInBoard() {
    this.postService.getPostsInBoard(this.boardId, this.page)
    .subscribe(posts => {
      this.posts = posts['items'];
      this.perPage = posts['perPage'];
      this.page = posts['page'];
      this.total = posts['total'];
    });
  }

  pageChanged(page: number) {
    this.postService.getPostsInBoard(this.boardId, page)
    .subscribe(posts => {
      this.posts = posts['items'];
      this.perPage = posts['perPage'];
      this.page = posts['page'];
      this.total = posts['total'];
    })
  }

}
