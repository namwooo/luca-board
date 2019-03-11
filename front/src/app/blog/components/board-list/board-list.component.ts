import { Component, OnInit } from '@angular/core';
import { Board } from 'src/app/blog/models/board';
import { BoardService } from 'src/app/api/board.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-board-list',
  templateUrl: './board-list.component.html',
  styleUrls: ['./board-list.component.css']
})
export class BoardListComponent implements OnInit {
  boards: Board[];
  selectedBoardId: number;

  constructor(
    private boardService: BoardService,
    private route: ActivatedRoute,
    ) {}

  ngOnInit() {
    this.route.paramMap.subscribe(
      params => {
        console.log(params)
        let id = +params['id']
        console.log(id)
        this.selectedBoardId = id
      }
    )
    this.getBoards();
  }

  getBoards(): void {
    this.boardService.getBoards()
    .subscribe(boards => this.boards = boards);
  }

  onClick(boardId: number) {
    this.selectedBoardId = boardId;
  }
}
