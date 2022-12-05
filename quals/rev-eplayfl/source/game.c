#include <stdlib.h>
#include <stdio.h>
#include "game.h"


static PlaydateAPI* pd = NULL;

#define ALPHABET_LEN 37
const char* alphabet = "_abcdefghijklmnopqrstuvwxyz0123456789";
#define FLAG_PREFIX "EPFL"
#define PREFIX_LEN 4
#define INNER_LEN 8
#define FLAG_LEN (PREFIX_LEN + INNER_LEN + 2)

// state
char flag[FLAG_LEN+1] = "0357txhn";
int flagIndex = 0;
uint64_t state = 0;

// background
LCDSprite *bgSprite = NULL;
LCDBitmap *bgImage = NULL;

const char* fontpath = "fonts/Asheville-Mono-Light-24-px";
LCDFont* font = NULL;

void setPDPtr(PlaydateAPI* p) {
	pd = p;
}


LCDBitmap *loadImageAtPath(const char *path) {
	const char *outErr = NULL;
	LCDBitmap *img = pd->graphics->loadBitmap(path, &outErr);
	return img;
}


static void drawBackgroundSprite(LCDSprite* sprite, PDRect bounds, PDRect drawrect) {
	pd->graphics->drawBitmap(bgImage, 0, 0, 0);
}


static void setupBackground(void) {
	bgSprite = pd->sprite->newSprite();

	bgImage = loadImageAtPath("images/background");
	pd->graphics->getBitmapData(bgImage, NULL, NULL, NULL, NULL, NULL);

	pd->sprite->setDrawFunction(bgSprite, drawBackgroundSprite);

	PDRect bgBounds = PDRectMake(0, 0, 400, 240);
	pd->sprite->setBounds(bgSprite, bgBounds);

	pd->sprite->setZIndex(bgSprite, 0);

	pd->sprite->addSprite(bgSprite);
}


void setupGame(void) {
	srand(pd->system->getSecondsSinceEpoch(NULL));
	
	const char* err;
	font = pd->graphics->loadFont(fontpath, &err);
	
	pd->graphics->setFont(font);

	setupBackground();
}


void checkCrank(void) {
	int change = (int)pd->system->getCrankChange() / 10;
	if (change > 1) {
		change = 1;
	} else if (change < -1) {
		change = -1;
	}
	
	if (flagIndex >= INNER_LEN)
		return;
	
	char letter = flag[flagIndex];
	int oldIndex = strchr(alphabet, letter) - alphabet;
	int newIndex = oldIndex + change;
	if (newIndex < 0) {
		newIndex = 0;
	} else if (newIndex >= ALPHABET_LEN) {
		newIndex = ALPHABET_LEN - 1;
	}
	
	change = newIndex - oldIndex;
	flag[flagIndex] = alphabet[newIndex];
	*((int8_t*)(&state) + flagIndex) += change;
	//pd->system->logToConsole("state = %llx", state);
}


void checkButtons(void) {
	PDButtons pushed;
	pd->system->getButtonState(NULL, &pushed, NULL);

	if ( pushed & kButtonA && flagIndex < INNER_LEN) {
		flagIndex++;
	}
	
	if (pushed & kButtonB && flagIndex > 0) {
		flagIndex--;
	}
}


#define CHAR_WIDTH 14
#define TEXT_WIDTH (FLAG_LEN*CHAR_WIDTH)
#define TEXT_HEIGHT 32

int x = (400-TEXT_WIDTH)/2;
int y = (240-TEXT_HEIGHT)/2;
uint8_t blinkCounter = 0;

void displayFlag(void) {
	pd->graphics->fillRect(x-5, y-5, TEXT_WIDTH+10, TEXT_HEIGHT+10, kColorWhite);
	
	if (flagIndex == INNER_LEN) {
		char* text = "I N V A L I D";
		if (state == 18376633736136491513u) {
			text = "  V A L I D  ";
		}
		pd->graphics->drawText(text, strlen(text), kASCIIEncoding, x, y);
		return;	
	}
	
	pd->graphics->drawText(FLAG_PREFIX "{", PREFIX_LEN + 1, kASCIIEncoding, x, y);
	pd->graphics->drawText(flag, FLAG_LEN, kASCIIEncoding, x + (PREFIX_LEN+1)*CHAR_WIDTH, y);
	pd->graphics->drawText("}", 1, kASCIIEncoding, x + (PREFIX_LEN+1+INNER_LEN)*CHAR_WIDTH, y);
	
	// cursor
	if (flagIndex < INNER_LEN && blinkCounter < 5) {
		pd->graphics->drawText("_", FLAG_LEN, kASCIIEncoding, x + (PREFIX_LEN+1+flagIndex)*CHAR_WIDTH, y+11);
	}
	blinkCounter = (blinkCounter+1) % 10;
}


// main update function
int update(void* ud) {
	checkButtons();
	checkCrank();

	pd->sprite->updateAndDrawSprites();
	
	displayFlag();

	return 1;
}
