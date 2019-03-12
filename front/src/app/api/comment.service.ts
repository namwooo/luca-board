import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Comment } from '../blog/models/comment';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  private baseUrl = 'http://localhost:5000/';

  constructor(
    private http: HttpClient,
  ) { }

  getCommentsInPost(idPost: number): Observable<Comment[]> {
    const url = this.baseUrl + `posts/${idPost}/comments`;
    return this.http.get<Comment[]>(url)
    .pipe(
      catchError(this.handleError<Comment[]>(`getPostsInBoard`))
      )
  }

  createComment(form: object, postId: number, parentCommentId: number): Observable<Comment> {
    let url;
    if (parentCommentId) {
      url = this.baseUrl + `comments?postId=${postId}&commentId=${parentCommentId}`;
    } else {
      url = this.baseUrl + `comments?postId=${postId}`;
    }

    return this.http.post<Comment>(url, form)
    .pipe(
      catchError(this.handleError<Comment>(`createComment`))
    )
  }

  updateComment(id: number, form: object): Observable<Comment> {
    let url = this.baseUrl + `comments/${id}`;
    return this.http.patch<Comment>(url, form)
    .pipe(
      catchError(this.handleError<Comment>(`updateComment`))
    )
  }

  deleteComment(commentId: number) {
    const url = this.baseUrl + `comments/${commentId}`;
    return this.http.delete(url)
    .pipe(
      catchError(this.handleError(`deleteComment`))
    )
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error('error'); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  withCredentials: true
};