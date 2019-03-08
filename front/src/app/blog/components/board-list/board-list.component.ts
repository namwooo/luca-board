import { Component, OnInit } from '@angular/core';
import { Board } from 'src/app/blog/models/board';
import { BoardService } from 'src/app/api/board.service';

@Component({
  selector: 'app-board-list',
  templateUrl: './board-list.component.html',
  styleUrls: ['./board-list.component.css']
})
export class BoardListComponent implements OnInit {
  boards: Board[];
  selectedBoardId: number;

  constructor(private boardService: BoardService) {}

  ngOnInit() {
    this.getBoards();
  }

  getBoards(): void {
    this.boardService.getBoards()
    .subscribe(boards => {
      this.boards = boards;
      // set ID of first board to ID of selected board
      this.selectedBoardId = boards[0].id;
    });
  }

  onClick(boardId: number) {
    this.selectedBoardId = boardId;
  }
}
