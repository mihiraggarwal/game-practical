import { test } from '@playwright/test';

test('spne', async ({ page }) => {
  await page.goto('http://localhost:5173/play');

  for (let i = 0; i < 15; i++) {
    // click on plus btn
    await page.getByTestId(`plus-node-${i}`).click();
    
    // click on move / payoff and fill
    if (i < 7) {
      await page.getByTestId(`move-${i}`).click()
      await page.getByTestId(`playernum-${i}`).fill(`${i == 0 || i > 2 ? 1 : 2}`)
    }
    else {
      await page.getByTestId(`payoff-${i}`).click()
      let filler = ""
      switch (i) {
        case 7:
          filler = "0,0"
          break;
        case 8:
          filler = "1,2"
          break;
        case 9:
          filler = "3,4"
          break;
        case 10:
          filler = "1,2"
          break;
        case 11:
          filler = "4,2"
          break;
        case 12:
          filler = "4,5"
          break;
        case 13:
          filler = "0,2"
          break;
        case 14:
          filler = "0,3"
          break;
      }
      await page.getByTestId(`payoffval-${i}`).fill(filler)
    }

    // click on enter
    if (i < 7) {
      await page.getByTestId(`move_enter_${i}`).click()
    }
    else {
      await page.getByTestId(`payoff_enter_${i}`).click()
    }

    if (i < 7) {
      // click on add action
      await page.getByTestId(`action-${i}`).click()

      // click on plus in actions
      await page.getByTestId(`plus_btn_${i}`).click()

      // add the actions
      for (let j = 0; j < 2; j++) {
        await page.getByTestId(`input-${i}-${j}`).fill(`${j}`)
      }

      // click on finish
      await page.getByTestId(`finish-${i}`).click()
    }
  }

  // add imperfections
  await page.getByTestId(`plus-node-4`).click({ button: 'right' });
  await page.getByTestId(`plus-node-5`).click({ button: 'right' });
  await page.getByText("Add Imperfect Info Set").click()

  // click on SPNE
  await page.getByText("SPNE").click()

});
