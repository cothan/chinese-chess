from orator.migrations import Migration


class CreateChessesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('chesses') as table:
            table.increments('id')

            table.string('token')

            table.string('user_id')
            table.foreign('user_id').references('email').on('users')

            table.string('oppo_id')
            table.foreign('oppo_id').references('email').on('users')

            table.string('next_id')

            table.string('move').nullable()
            table.boolean('completed')

            table.string('owner')

            table.string('winner').nullable()
            table.foreign('winner').references('email').on('users')

            table.string('msg').nullable()

            table.integer('last_move_timestamp').unsigned()

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('chesses')
