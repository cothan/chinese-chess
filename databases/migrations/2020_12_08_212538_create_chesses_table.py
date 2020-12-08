from orator.migrations import Migration


class CreateChessesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('chesses') as table:
            table.increments('id')

            table.string('token')

            table.integer('user_id').unsigned()
            table.foreign('user_id').references('id').on('users')

            table.integer('oppo_id').unsigned()
            table.foreign('oppo_id').references('id').on('users')

            table.integer('next_id').unsigned()

            table.string('move').nullable()
            table.boolean('completed')
            table.integer('last_move_timestamp').unsigned()

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('chesses')
