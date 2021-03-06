/*********************************************
 *  agent.c
 *  Sample Agent for Text-Based Adventure Game
 *  COMP3411 Artificial Intelligence
 *  UNSW Session 1, 2016
*/

#include <stdio.h>
#include <stdlib.h>

#include "pipe.h"

int   pipe_fd;
FILE* in_stream;
FILE* out_stream;

char view[5][5];
char world[80][80];
int in_world[80][80];
const int EAST   = 0;
const int NORTH  = 1;
const int WEST   = 2;
const int SOUTH  = 3;
int false = 0;
int true = 1; 
int dirn = 1; //initial direction is NORTH
int stone = 0;
int colum = 60;	  //the colume,row number of the world and in_world world[colmn][row]
int row =60;
/* new by I */
char hang_out() {
	char action;
	if (isblank(view[1][2]) || view[1][2] == 'o') {
		if (view[1][2] == 'o'){
			stone = true;
		}
		action = 'rf';
		
		record_to_world();
		return action;		
	}
	else if (isblank(view[2][3]) || view[2][3]== 'o') {
		action = 'fr';
		if (dirn == EAST){
			dirn = SOUTH;
		}		
		else{
			dirn = dirn -1;
		}
	}
	else {
		action = 'lf';
		if (dirn == SOUTH) {
			dirn = EAST;
		}
		else{
			dirn = dirn + 1;
		}
	}
	return action;
}

void record_to_world(){ //save the view into the world[][] which is world model
 int i;
 int r;
 int c;
 switch(dirn) {
 	case 1: { 
		c = -3;r = 0;break;
	}
	case 3: {
		c = 3;r = 0;break;
	}
	case 2: {
		c = 0;r = -3;break;
	}	
	case 0: {
		c = 0;r = 3;break;
	}
 }	
	
 for(i=-2;i<3;i++ ){
	if (r == 0) {
		if (in_world[colum + c][row+i] != false ){
			world[colum + c][row+i] = view[0][2+i];
			in_world[colum + c][row+i] = true;
		}
	}
	if (c == 0) {
		if (in_world[colum + i][row+ r] != false) {
			world[colum + i][row+ r] = view[0][2+i];
			in_world[colum + i][row + r] = true;
		}
	}
 }
}
	
	
	
	



char get_action( char view[5][5] ) {

  // REPLACE THIS CODE WITH AI TO CHOOSE ACTION

  int ch=0;
int row1;
int col1;
  printf("Enter Action(s): ");
//int row,col;
/*printf("\n");
      for (row1=50; row1<90; row1++)
    {
        //输出当前行的元素
        for (col1=50; col1<90; col1++){
            putchar(world[row1][col1]);
	}
        //换行
        printf("\n");
    }
*/
  while(( ch = getchar()) != -1 ) { // read character from keyboard

    switch( ch ) { // if character is a valid action, return it
    case 'F': case 'L': case 'R': case 'C': case 'U':
    case 'f': case 'l': case 'r': case 'c': case 'u':
      return(hang_out());
    }
  }
  return 0;
}


void print_view()
{
  int i,j;

  printf("\n+-----+\n");
  for( i=0; i < 5; i++ ) {
    putchar('|');
    for( j=0; j < 5; j++ ) {
      if(( i == 2 )&&( j == 2 )) {
        putchar( '^' );
      }
      else {
        putchar( view[i][j] );
      }
    }
    printf("|\n");
  }
  printf("+-----+\n");
}

int main( int argc, char *argv[] )
{
  char action;
  int sd;
  int ch;
  int i,j;

  if ( argc < 3 ) {
    printf("Usage: %s -p port\n", argv[0] );
    exit(1);
  }

    // open socket to Game Engine
  sd = tcpopen("localhost", atoi( argv[2] ));

  pipe_fd    = sd;
  in_stream  = fdopen(sd,"r");
  out_stream = fdopen(sd,"w");

  while(1) {
      // scan 5-by-5 wintow around current location
    for( i=0; i < 5; i++ ) {
      for( j=0; j < 5; j++ ) {
        if( !(( i == 2 )&&( j == 2 ))) {
          ch = getc( in_stream );
          if( ch == -1 ) {
            exit(1);
          }
          view[i][j] = ch;
        }
      }
    }

    print_view(); // COMMENT THIS OUT BEFORE SUBMISSION
    action = get_action( view );
    putc( action, out_stream );
    fflush( out_stream );
  }

  return 0;
}
