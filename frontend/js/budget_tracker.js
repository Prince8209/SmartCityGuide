/**
 * Budget Tracker Module
 * Handles budget calculations and expense tracking for the Features page demo
 */

const BudgetTracker = {
    state: {
        totalBudget: 0,
        days: 0,
        expenses: [],
        categories: {
            'Accommodation': 0,
            'Local Transport': 0,
            'Food & Dining': 0,
            'Activities': 0,
            'Shopping': 0
        }
    },

    STORAGE_KEY: 'scg_budget_tracker_v1',

    init: function (defaultBudget = 15000, defaultDays = 3) {
        // Try to load from storage
        const saved = localStorage.getItem(this.STORAGE_KEY);
        if (saved) {
            try {
                this.state = JSON.parse(saved);
                console.log('Budget loaded from storage');
            } catch (e) {
                console.error('Failed to parse saved budget', e);
                this.resetState(defaultBudget, defaultDays);
            }
        } else {
            this.resetState(defaultBudget, defaultDays);
        }
    },

    resetState: function (defaultBudget, defaultDays) {
        this.state = {
            totalBudget: defaultBudget,
            days: defaultDays,
            expenses: [],
            categories: {
                'Accommodation': 0,
                'Local Transport': 0,
                'Food & Dining': 0,
                'Activities': 0,
                'Shopping': 0
            }
        };
        // Add dummy data only on fresh reset
        this.addExpense('Accommodation', 4500, 'Hotel Booking (3 Nights)');
        this.addExpense('Food & Dining', 1200, 'Lunch & Dinner Day 1');
        this.addExpense('Local Transport', 500, 'Taxi from Airport');
    },

    saveState: function () {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.state));
    },

    addExpense: function (category, amount, description) {
        this.state.expenses.push({
            id: Date.now(),
            category,
            amount,
            description,
            time: new Date()
        });

        if (this.state.categories[category] !== undefined) {
            this.state.categories[category] += amount;
        } else {
            this.state.categories[category] = amount;
        }
        this.saveState();
    },

    removeExpense: function (id) {
        const index = this.state.expenses.findIndex(e => e.id === id);
        if (index !== -1) {
            const expense = this.state.expenses[index];
            if (this.state.categories[expense.category] !== undefined) {
                this.state.categories[expense.category] -= expense.amount;
            }
            this.state.expenses.splice(index, 1);
            this.saveState();
            this.renderTracker('budgetTrackerDemo');
        }
    },

    clearAll: function () {
        if (confirm('Are you sure you want to clear all data?')) {
            this.state.expenses = [];
            this.state.categories = {
                'Accommodation': 0,
                'Local Transport': 0,
                'Food & Dining': 0,
                'Activities': 0,
                'Shopping': 0
            };
            this.saveState();
            this.renderTracker('budgetTrackerDemo');
        }
    },

    getTotalSpent: function () {
        return this.state.expenses.reduce((sum, item) => sum + item.amount, 0);
    },

    getRemaining: function () {
        return this.state.totalBudget - this.getTotalSpent();
    },

    updateBudget: function (amount) {
        this.state.totalBudget = parseInt(amount) || 0;
        this.saveState();
        this.renderTracker('budgetTrackerDemo');
    },

    renderTracker: function (containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const totalSpent = this.getTotalSpent();
        const remaining = this.getRemaining();
        const percentUsed = this.state.totalBudget > 0 ? Math.min((totalSpent / this.state.totalBudget) * 100, 100) : 100;

        // Colors
        let progressColor = '#48bb78'; // Green
        if (percentUsed > 70) progressColor = '#ecc94b'; // Yellow
        if (percentUsed > 90) progressColor = '#f56565'; // Red

        container.innerHTML = `
            <div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto;">
                
                <!-- Controls -->
                <div style="display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; justify-content: center;">
                    <div style="flex: 1; min-width: 200px;">
                        <label style="display: block; color: #718096; margin-bottom: 0.5rem;">Total Budget (₹)</label>
                        <input type="number" value="${this.state.totalBudget}" 
                            onchange="BudgetTracker.updateBudget(this.value)"
                            style="width: 100%; padding: 0.8rem; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 1rem;">
                    </div>
                    <div style="flex: 1; min-width: 200px; display: flex; align-items: flex-end;">
                        <div style="background: #f7fafc; padding: 1rem; border-radius: 8px; width: 100%; border: 1px solid #e2e8f0;">
                            <span style="color: #718096;">Remaining:</span>
                            <span style="font-size: 1.5rem; font-weight: 700; color: ${remaining >= 0 ? '#48bb78' : '#f56565'}; display: block;">
                                ₹${remaining.toLocaleString()}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div style="margin-bottom: 2rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; color: #718096; font-size: 0.9rem;">
                        <span>0%</span>
                        <span>50%</span>
                        <span>100%</span>
                    </div>
                    <div style="height: 12px; background: #edf2f7; border-radius: 6px; overflow: hidden;">
                        <div style="width: ${percentUsed}%; height: 100%; background: ${progressColor}; transition: width 0.3s ease;"></div>
                    </div>
                </div>

                <!-- Expense Form -->
                <form id="addExpenseForm" onsubmit="event.preventDefault(); BudgetTracker.handleSubmit(this);" 
                    style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;">
                    <h4 style="margin-bottom: 1rem; color: #2d3748;">Add New Expense</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                        <select name="category" required style="padding: 0.8rem; border: 1px solid #cbd5e0; border-radius: 6px;">
                            ${Object.keys(this.state.categories).map(c => `<option value="${c}">${c}</option>`).join('')}
                        </select>
                        <input type="text" name="desc" placeholder="Description" required style="padding: 0.8rem; border: 1px solid #cbd5e0; border-radius: 6px;">
                        <input type="number" name="amount" placeholder="Amount (₹)" required style="padding: 0.8rem; border: 1px solid #cbd5e0; border-radius: 6px;">
                    </div>
                    <button type="submit" class="btn-city" style="width: 100%;">
                        <i class="fas fa-plus"></i> Add Expense
                    </button>
                </form>

                <!-- Expense List -->
                <div>
                    <h4 style="margin-bottom: 1rem; color: #2d3748; display: flex; justify-content: space-between; align-items: center;">
                        Recent Expenses
                        <div style="font-size: 0.9rem; font-weight: 400;">
                            <span style="color: #718096; margin-right: 10px;">Total Spent: ₹${totalSpent.toLocaleString()}</span>
                            <button onclick="BudgetTracker.clearAll()" style="color: #e53e3e; background: none; border: none; cursor: pointer; text-decoration: underline;">Clear All</button>
                        </div>
                    </h4>
                    <div style="max-height: 300px; overflow-y: auto;">
                        ${this.state.expenses.length === 0 ?
                '<p style="text-align: center; color: #a0aec0; padding: 1rem;">No expenses yet</p>' :
                this.state.expenses.slice().reverse().map(item => `
                                <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; border-bottom: 1px solid #edf2f7;">
                                    <div>
                                        <div style="font-weight: 600; color: #2d3748;">${item.description}</div>
                                        <div style="font-size: 0.85rem; color: #718096;">
                                            <span style="display: inline-block; background: #e2e8f0; padding: 2px 8px; border-radius: 12px; margin-right: 0.5rem;">${item.category}</span>
                                            ${new Date(item.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </div>
                                    </div>
                                    <div style="display: flex; align-items: center; gap: 1rem;">
                                        <span style="font-weight: 700; color: #e53e3e;">-₹${item.amount.toLocaleString()}</span>
                                        <button onclick="BudgetTracker.removeExpense(${item.id})" style="background: none; border: none; color: #cbd5e0; cursor: pointer;">
                                            <i class="fas fa-times"></i>
                                        </button>
                                    </div>
                                </div>
                            `).join('')
            }
                    </div>
                </div>
            </div>
        `;
    },

    handleSubmit: function (form) {
        const category = form.category.value;
        const desc = form.desc.value;
        const amount = parseInt(form.amount.value);

        if (category && desc && amount) {
            this.addExpense(category, amount, desc);
            form.reset();
            this.renderTracker('budgetTrackerDemo');
        }
    }
};
