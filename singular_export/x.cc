/*
 * =====================================================================================
 *
 *       Filename:  x.cc
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  26/10/17 17:22:03
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */
#define	IPARITH			/*  */
#define	SINGULAR_4_2			/*  */
#define	HAVE_PLURAL			/*  */
#define	OLD_RES			/*  */
//#define	GENTABLE			/*  */
#define	IPCONV			/*  */
#define	IPASSIGN			/*  */
#define	HAVE_GETTIMEOFDAY			/*  */
#include "table.h"

typedef struct {
  char *name;
  short alias;
  short tokval;
  short toktype;
} cmdnames;
