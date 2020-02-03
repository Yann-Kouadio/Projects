// BUDGET CONTROLLER
let budgetController = (function() {

    let Budget = function(month, year) {
        this.month = month;
        this.year = year;
        this.allItems = {
            exp: [],
            inc: []
        };
        this.totals = {
            exp: 0,
            inc: 0
        };
        this.budget = 0;
        this.percentage = -1;
    };

    let Expense = function(id, description, value) {
        this.id = id;
        this.description = description;
        this.value = value;
        this.percentage = -1;
    };

    Expense.prototype.calcPercentage = function(totalIncome) {
        if (totalIncome > 0) {
            this.percentage = Math.round((this.value / totalIncome) * 100);
        } else {
            this.percentage = -1;
        }
    };

    Expense.prototype.getPercentage = function() {
        return this.percentage;
    };

    let Income = function(id, description, value) {
        this.id = id;
        this.description = description;
        this.value = value;
    };

    let calculateTotal = function(budgetObj, type) {
        let sum = 0;

        budgetObj.allItems[type].forEach(function(cur) {
            sum += cur.value;
        });

        budgetObj.totals[type] = sum;
    };

    let createNewBudget = function (month, year) {
        let budget = new Budget(month, year);

        allBudgets.push(new Budget(month, year));

        localStorage.setItem('allBudgets', JSON.stringify(allBudgets));

        return budget;
    };

    let updateAllBudgetStorage =  function(budgetObj) {
        const allBudgetStorage = JSON.parse(localStorage.getItem('allBudgets'));

        // Find the index of the current object
        const index = allBudgetStorage.findIndex( el => {return  el.month === budgetObj.month && el.year === budgetObj.year});

        // Update it
        allBudgetStorage[index] = budgetObj;

        // Update the local storage
        localStorage.setItem('allBudgets', JSON.stringify(allBudgetStorage))
    };

    const storeBudget = JSON.parse(localStorage.getItem('allBudgets'));

    let allBudgets = [];

    if (storeBudget) {
        allBudgets = storeBudget;
    }

    return {
        init: function(month, year) {
            // Verify if the budget exist if not we will create it
            let budget;

            if (allBudgets.length > 0) {

                function searchBudgetHelper (i, exist, budget_ = null) {
                    if (i >= allBudgets.length) {
                        !exist ? budget = createNewBudget(month, year) : budget = budget_;
                    } else {
                        let item = allBudgets[i];

                        if (item.month === month && item.year === year) {
                            exist = true;
                            budget_ = allBudgets[i];
                            i = allBudgets.length;
                        } else {
                            i += 1;
                        }

                        searchBudgetHelper(i, exist, budget_);
                    }
                }

                searchBudgetHelper(0, false);

            }else {
                budget = createNewBudget(month, year);
            }

            return budget;
        },

        getBudgetObj: function(month, year) {
            let budget;

            if (month < 0 || year < 0) {
                budget = createNewBudget('--', '--')
            } else {
                allBudgets.forEach( function (item) {
                    item.month === month && item.year === year ? budget = item : null;
                });
            }

            return budget;
        },

        addItem: function(budgetObj, type, des, val) {
            let newItem, ID;

            //[1 2 3 4 5], next ID = 6
            //[1 2 4 6 8], next ID = 9
            // ID = last ID + 1

            // Create new ID
            if (budgetObj.allItems[type].length > 0) {
                ID = budgetObj.allItems[type][budgetObj.allItems[type].length - 1].id + 1;
            } else {
                ID = 0;
            }

            // Create new item based on 'inc' or 'exp' type
            if (type === 'exp') {
                newItem = new Expense(ID, des, val);
            } else if (type === 'inc') {
                newItem = new Income(ID, des, val);
            }

            // Push it into our data structure
            budgetObj.allItems[type].push(newItem);

            // Return the new element
            return newItem;
        },

        deleteItem: function(budgetObj, type, id) {
            let ids, index;

            // id = 6
            //data.allItems[type][id];
            // ids = [1 2 4  8]
            //index = 3

            ids = budgetObj.allItems[type].map(function(current) {
                return current.id;
            });

            index = ids.indexOf(id);

            if (index !== -1) {
                budgetObj.allItems[type].splice(index, 1);
            }

        },

        calculateBudget: function(budgetObj) {

            // calculate total income and expenses
            calculateTotal(budgetObj, 'exp');
            calculateTotal(budgetObj, 'inc');

            // Calculate the budget: income - expenses
            budgetObj.budget = budgetObj.totals.inc - budgetObj.totals.exp;

            // calculate the percentage of income that we spent
            if (budgetObj.totals.inc > 0) {
                budgetObj.percentage = Math.round((budgetObj.totals.exp / budgetObj.totals.inc) * 100);
            } else {
                budgetObj.percentage = -1;
            }

            // Expense = 100 and income 300, spent 33.333% = 100/300 = 0.3333 * 100

            // Add the final budget obj to the local storage
            updateAllBudgetStorage(budgetObj);
        },

        calculatePercentages: function(budgetObj) {

            /*
            a=20
            b=10
            c=40
            income = 100
            a=20/100=20%
            b=10/100=10%
            c=40/100=40%
            */

            budgetObj.allItems.exp.forEach(function(cur) {
                cur.calcPercentage(budgetObj.totals.inc);
            });
        },

        getPercentages: function(budgetObj) {
            let allPerc = budgetObj.allItems.exp.map(function(cur) {
                return cur.getPercentage();
            });
            return allPerc;
        }

        // getBudget: function(budgetObj) {
        //     return {
        //         budget: budgetObj.budget,
        //         totalInc: budgetObj.totals.inc,
        //         totalExp: budgetObj.totals.exp,
        //         percentage: budgetObj.percentage
        //     };
        // },



    };

})();



// UI CONTROLLER
let UIController = (function() {

    let DOMstrings = {
        inputType: '.add__type',
        inputDescription: '.add__description',
        inputValue: '.add__value',
        inputBtn: '.add__btn',
        incomeContainer: '.income__list',
        expensesContainer: '.expenses__list',
        budgetLabel: '.budget__value',
        incomeLabel: '.budget__income--value',
        expensesLabel: '.budget__expenses--value',
        percentageLabel: '.budget__expenses--percentage',
        container: '.container',
        expensesPercLabel: '.item__percentage',
        dateLabel: '.budget__title--month',
        containerDate: '.container__date',
        selectNewDate: '.select__newDate',
        selectBtn: '.select__btn',
        selectMonth: '.select__month',
        selectYear: '.select__year',
        containerContent: '.container__content'

    };

    let formatNumber = function(num, type) {
        let numSplit, int, dec;
        /*
            + or - before number
            exactly 2 decimal points
            comma separating the thousands

            2310.4567 -> + 2,310.46
            2000 -> + 2,000.00
            */

        num = Math.abs(num);
        num = num.toFixed(2);

        numSplit = num.split('.');

        int = numSplit[0];
        if (int.length > 3) {
            int = int.substr(0, int.length - 3) + ',' + int.substr(int.length - 3, 3); //input 23510, output 23,510
        }

        dec = numSplit[1];

        return (type === 'exp' ? '-' : '+') + ' ' + int + '.' + dec;

    };

    let nodeListForEach = function(list, callback) {
        for (let i = 0; i < list.length; i++) {
            callback(list[i], i);
        }
    };

    return {
        init: function(budgetObj) {
            document.querySelector(DOMstrings.containerContent).classList.add('hide');

            this.displayBudget(budgetObj);
        },

        hideOrShowInputFields: function () {
            // document.querySelector(DOMstrings.containerDate).style.display = 'block';
            // document.querySelector(DOMstrings.containerContent).style.display = 'none';

            document.querySelector(DOMstrings.containerDate).classList.toggle('hide');
            document.querySelector(DOMstrings.containerContent).classList.toggle('hide');
            document.querySelector(DOMstrings.inputType).selectedIndex = "0";
        },

        getInput: function() {
            return {
                type: document.querySelector(DOMstrings.inputType).value, // Will be either inc or exp
                description: document.querySelector(DOMstrings.inputDescription).value,
                value: parseFloat(document.querySelector(DOMstrings.inputValue).value)
            };
        },

        getSelectValue: function() {
            return {
                month: parseInt(document.querySelector(DOMstrings.selectMonth).value),
                year: parseInt(document.querySelector(DOMstrings.selectYear).value)
            };
        },

        loadAllItems: function(budgetObj) {

            let loader = function(obj, callback) {
              return function (type) {
                  obj.allItems[type].forEach( function (curr) {
                      callback(curr, type);
                  });
              };
            };

            // Here i was trying to use bind but i didn't work and i don't understand why, maybe i cannot use bind here
            // I was trying something like that :
            // let itemsLoader = loader.bind(this, budgetObj, this.addListItem);
            // itemsLoader('inc')
            // itemsLoader('exp')

            // Add the different type for the load
            loader(budgetObj, this.addListItem)('inc');
            loader(budgetObj, this.addListItem)('exp');
        },

        addListItem: function(obj, type) {
            let html, newHtml, element;
            // Create HTML string with placeholder text

            if (type === 'inc') {
                element = DOMstrings.incomeContainer;

                html = '<div class="item clearfix" id="inc-%id%"> <div class="item__description">%description%</div><div class="right clearfix"><div class="item__value">%value%</div><div class="item__delete"><button class="item__delete--btn"><i class="ion-ios-close-outline"></i></button></div></div></div>';
            } else if (type === 'exp') {
                element = DOMstrings.expensesContainer;

                html = '<div class="item clearfix" id="exp-%id%"><div class="item__description">%description%</div><div class="right clearfix"><div class="item__value">%value%</div><div class="item__percentage">21%</div><div class="item__delete"><button class="item__delete--btn"><i class="ion-ios-close-outline"></i></button></div></div></div>';
            }

            // Replace the placeholder text with some actual data
            newHtml = html.replace('%id%', obj.id);
            newHtml = newHtml.replace('%description%', obj.description);
            newHtml = newHtml.replace('%value%', formatNumber(obj.value, type));

            // Insert the HTML into the DOM
            document.querySelector(element).insertAdjacentHTML('beforeend', newHtml);
        },

        deleteListItem: function(selectorID) {
            let el = document.getElementById(selectorID);
            el.parentNode.removeChild(el);
        },

        clearAllItems: function() {
            const incomeNode = document.querySelector(DOMstrings.incomeContainer);
            const expenseNode = document.querySelector(DOMstrings.expensesContainer);

            function deleteAllChild(parentNode) {
                while (parentNode.firstChild) {
                    parentNode.removeChild(parentNode.firstChild);
                }
            }

            deleteAllChild(incomeNode);
            deleteAllChild(expenseNode);
        },

        clearFields: function() {
            let fields, fieldsArr;

            fields = document.querySelectorAll(DOMstrings.inputDescription + ', ' + DOMstrings.inputValue);

            fieldsArr = Array.prototype.slice.call(fields);

            fieldsArr.forEach(function(current, index, array) {
                current.value = "";
            });

            fieldsArr[0].focus();
        },

        displayBudget: function(obj, updateDate = true) {
            let type;
            obj.budget > 0 ? type = 'inc' : type = 'exp';

            document.querySelector(DOMstrings.budgetLabel).textContent = formatNumber(obj.budget, type);
            document.querySelector(DOMstrings.incomeLabel).textContent = formatNumber(obj.totals.inc, 'inc');
            document.querySelector(DOMstrings.expensesLabel).textContent = formatNumber(obj.totals.exp, 'exp');

            if (obj.percentage > 0) {
                document.querySelector(DOMstrings.percentageLabel).textContent = obj.percentage + '%';
            } else {
                document.querySelector(DOMstrings.percentageLabel).textContent = '---';
            }

            updateDate ? this.displayMonth(obj.month, obj.year) : null;
        },

        displayPercentages: function(percentages) {

            let fields = document.querySelectorAll(DOMstrings.expensesPercLabel);

            let nodeListForEach = function(list, callback) {
                for (let i = 0; i < list.length; i++) {
                    callback(list[i], i);
                }
            };

            nodeListForEach(fields, function(current, index) {

                if (percentages[index] > 0) {
                    current.textContent = percentages[index] + '%';
                } else {
                    current.textContent = '---';
                }
            });

        },

        displayMonth: function(month, year) {
            // let now, months, month, year;

            // now = new Date();
            //let christmas = new Date(2016, 11, 25);

            const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            month = month > 0 ? months[month-1] : month;

            document.querySelector(DOMstrings.dateLabel).textContent = month + ' ' + year;
        },

        changedType: function() {

            let fields = document.querySelectorAll(
                DOMstrings.inputType + ',' +
                DOMstrings.inputDescription + ',' +
                DOMstrings.inputValue);

            nodeListForEach(fields, function(cur) {
                cur.classList.toggle('red-focus');
            });

            document.querySelector(DOMstrings.inputBtn).classList.toggle('red');
        },

        getDOMstrings: function() {
            return DOMstrings;
        }
    };

})();


// GLOBAL APP CONTROLLER
let controller = (function(budgetCtrl, UICtrl) {

    let setupEventListeners = function() {
        let DOM = UICtrl.getDOMstrings();

        document.querySelector(DOM.inputBtn).addEventListener('click', ctrlAddItem);

        document.addEventListener('keypress', function(event) {
            if (event.keyCode === 13 || event.which === 13) {

                const containerDate = document.querySelector(DOM.containerDate);
                const  containerContent = document.querySelector(DOM.containerContent);

                if (window.getComputedStyle(containerDate).display === "none") {
                    ctrlAddItem();
                } else if (window.getComputedStyle(containerContent).display === "none") {
                    createOrLoadBudget();
                }
            }
        });

        document.querySelector(DOM.container).addEventListener('click', ctrlDeleteItem);

        document.querySelector(DOM.inputType).addEventListener('change', UICtrl.changedType);

        document.querySelector(DOM.selectNewDate).addEventListener('click', UICtrl.hideOrShowInputFields);
        document.querySelector(DOM.selectBtn).addEventListener('click', createOrLoadBudget);
    };

    let createOrLoadBudget = function () {
        // Get value from select
        const selectInput = UICtrl.getSelectValue();

        if (selectInput.month > 0 && selectInput.year > 0) {
            // Display the input fields
            UICtrl.hideOrShowInputFields();

            // Create or load budget
            const budget = budgetCtrl.init(selectInput.month, selectInput.year);

            // Update the budget UI
            UICtrl.displayBudget(budget);

            // Clear the items component in the UI
            UICtrl.clearAllItems();

            // Load the new budget component in the UI
            UICtrl.loadAllItems(budget);
        }
    };

    let updateBudget = function(budgetObj) {

        // 1. Calculate the budget
        budgetCtrl.calculateBudget(budgetObj);

        // 2. Return the budget
        // let budget = budgetCtrl.getBudget(budgetObj);

        // 3. Display the budget on the UI
        UICtrl.displayBudget(budgetObj, updateDate = false);
    };

    let updatePercentages = function(budgetObj) {
        // 1. Calculate percentages
        budgetCtrl.calculatePercentages(budgetObj);

        // 2. Read percentages from the budget controller
        let percentages = budgetCtrl.getPercentages(budgetObj);

        // 3. Update the UI with the new percentages
        UICtrl.displayPercentages(percentages);
    };

    let ctrlAddItem = function() {
        let input, newItem;

        // Get the current budget
        const budgetObj = budgetCtrl.getBudgetObj(UICtrl.getSelectValue().month, UICtrl.getSelectValue().year);

        // 1. Get the field input data
        input = UICtrl.getInput();

        if (input.description !== "" && !isNaN(input.value) && input.value > 0) {
            // 2. Add the item to the budget controller
            newItem = budgetCtrl.addItem(budgetObj, input.type, input.description, input.value);

            // 3. Add the item to the UI
            UICtrl.addListItem(newItem, input.type);

            // 4. Clear the fields
            UICtrl.clearFields();

            // 5. Calculate and update budget
            updateBudget(budgetObj);

            // 6. Calculate and update percentages
            updatePercentages(budgetObj);
        }
    };

    let ctrlDeleteItem = function(event) {
        let itemID, splitID, type, ID;

        // Get the current budget
        const budgetObj = budgetCtrl.getBudgetObj(UICtrl.getSelectValue().month, UICtrl.getSelectValue().year);

        itemID = event.target.parentNode.parentNode.parentNode.parentNode.id;

        if (itemID) {

            //inc-1
            splitID = itemID.split('-');
            type = splitID[0];
            ID = parseInt(splitID[1]);

            // 1. delete the item from the data structure
            budgetCtrl.deleteItem(budgetObj, type, ID);

            // 2. Delete the item from the UI
            UICtrl.deleteListItem(itemID);

            // 3. Update and show the new budget
            updateBudget(budgetObj);

            // 4. Calculate and update percentages
            updatePercentages(budgetObj);
        }
    };


    return {
        init: function() {
            console.log('Application has started.');
            UICtrl.init(budgetCtrl.getBudgetObj(-1, -1));
            setupEventListeners();
        }
    };

})(budgetController, UIController);


controller.init();
